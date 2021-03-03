#!/usr/bin/env python
# -*- coding: utf-8 vi:et

import sys, io, os, logging
import re
import json
import tempfile
import subprocess

import urllib.request, urllib.error


logger = logging.getLogger(__name__)


__all__ = (
 "get_remote",
 "create_release",
 "download_default_release_asset",
 "upload_release_asset",
 "update_release_with_mirror_urls",
 "get_repo_releases",
)


def get_remote(target_repo, cfg_root):
    """
    Get the organization/repo_name from a repo
    """

    remote = cfg_root.get("remote", "origin")

    cmd = ["git", "config", f"remote.{remote}.url"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, cwd=target_repo)
    url = res.stdout.rstrip().decode()

    m = re.match(r"^git@github.com:(?P<repo>\S+)(\.git)?$", url)
    if m is not None:
        return m.group("repo")

    m = re.match(r"^https://github.com/(?P<repo>\S+)(\.git)?$", url)
    if m is not None:
        return m.group("repo")

    raise ValueError(url)


def create_release(github_repo, git_tag, gh_token, cfg_root):
    """
    Create a new release within the target repository.
    :return: release metadata with id on success.
    """

    logger.info("Creating a new release for %s at revision %s", github_repo, git_tag)

    url = "https://api.github.com/repos/{}/releases".format(github_repo)

    headers = {
     "Authorization": "token {}".format(gh_token),
     "Content-Type": "application/json",
    }

    root = {
     "tag_name": git_tag,
     "name": git_tag,
     "draft": False,
     "prerelease": False,
    }

    payload = json.dumps(root).encode("utf-8")

    req = urllib.request.Request(url, headers=headers, method="POST", data=payload)

    with urllib.request.urlopen(req) as resp:
        if resp.getcode() != 201:
            raise RuntimeError(
                "Bad response: {} / {}".format(resp.getcode(), resp.read())
            )
        ret = json.loads(resp.read().decode("utf-8"))
        logger.debug("ret: %s", ret)
        release_id = ret["id"]

    logger.info("Release (id:%s) successfully createad.", release_id)
    return release_id


def download_default_release_asset(github_repo, release_id, gh_token, target_dir):
    """
    Download the default asset of a given release
    :return: relative path to downloaded file.
    """

    logger.info("Downloading release default artifact...")

    url = f"https://api.github.com/repos/{github_repo}/releases/{release_id}"

    headers = {
     "Authorization": f"token {gh_token}",
     "Content-Type": "application/octet-stream",
    }

    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req) as resp:
        if resp.getcode() != 200:
            raise RuntimeError(
                "Bad response: {} / {}".format(resp.getcode(), resp.read())
            )
        ret = json.loads(resp.read().decode("utf-8"))
        logger.debug("ret: %s", ret)

        pnpv = "{}-{}".format(github_repo.split("/")[-1], ret["tag_name"])

        asset_name = f"{pnpv}.zip"

        downloaded_asset_path = os.path.join(target_dir, asset_name)

        urllib.request.urlretrieve(
         ret["zipball_url"], downloaded_asset_path, #reporthook=...
        )

    return downloaded_asset_path


def upload_release_asset(github_repo, release_id, asset_path, gh_token):
    """
    Uploads a release asset to a target release.
    :return: Download link of the uploaded asset.
    """
    logger.info("Uploading default release asset to sct-data/%s", github_repo)

    asset_name = os.path.basename(asset_path)

    url = f"https://uploads.github.com/repos/{github_repo}/releases/{release_id}/assets?name={asset_name}"

    headers = {
     "Authorization": f"token {gh_token}",
     "Content-Type": "application/octet-stream",
    }

    with io.open(asset_path, "rb") as fi:
        payload = fi.read()

    req = urllib.request.Request(url, headers=headers, method="POST", data=payload)
    with urllib.request.urlopen(req) as resp:
        if resp.getcode() != 201:
            raise RuntimeError(
                "Bad response: {} / {}".format(resp.getcode(), resp.read())
            )
        ret = json.loads(resp.read().decode("utf-8"))
        logger.debug("ret: %s", ret)

    logger.info("Release asset uploaded successfully.")
    return ret["browser_download_url"]


def update_release_with_mirror_urls(github_repo, release_id, gh_token, urls):
    """
    Include osf download url (in case osf upload was performed) to the Github release
    """
    logger.info("Uploading release with OSF download url.")

    url = f"https://api.github.com/repos/{github_repo}/releases/{release_id}"

    headers = {
     "Authorization": f"token {gh_token}",
     "Content-Type": "application/json",
    }

    body = "Asset also available at {}".format(urls)

    root = {"body": body}

    payload = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, headers=headers, method="PATCH", data=payload)

    with urllib.request.urlopen(req) as resp:
        if resp.getcode() != 200:
            raise RuntimeError(
                "Bad response: {} / {}".format(resp.getcode(), resp.read())
            )
        ret = json.loads(resp.read().decode("utf-8"))

    return ret

def get_org_repos(org):
    url = f"https://api.github.com/orgs/{org}/repos"

    headers = {
     "Content-Type": "application/json",
    }

    req = urllib.request.Request(url, headers=headers, method="GET")

    with urllib.request.urlopen(req) as resp:
        if resp.getcode() != 200:
            raise RuntimeError(
                "Bad response: {} / {}".format(resp.getcode(), resp.read())
            )
        ret = json.loads(resp.read().decode("utf-8"))
        logger.debug("ret: %s", ret)

        return [ repo["name"] for repo in ret ]


def get_repo_tags(github_repo):
    url = f"https://api.github.com/repos/{github_repo}/tags"

    headers = {
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(url, headers=headers, method="GET")

    with urllib.request.urlopen(req) as resp:
        if resp.getcode() != 200:
            raise RuntimeError(
                "Bad response: {} / {}".format(resp.getcode(), resp.read())
            )
        ret = json.loads(resp.read().decode("utf-8"))
        logger.debug("ret: %s", ret)

        return [ tag["name"] for tag in ret ]

def get_repo_releases(github_repo):
    url = f"https://api.github.com/repos/{github_repo}/releases"
    req = urllib.request.Request(url)

    with urllib.request.urlopen(req) as resp:
        if resp.getcode() != 200:
            msg = "Bad response: {} / {}".format(resp.getcode(), resp.read())
            raise RuntimeError(msg)
        ret = json.loads(resp.read().decode("utf-8"))
        return { rel["tag_name"]: rel["id"] for rel in ret }, { rel["id"]: rel for rel in ret }
