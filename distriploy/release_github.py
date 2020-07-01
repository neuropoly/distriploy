#!/usr/bin/env python
# -*- coding: utf-8 vi:et

import sys, io, os, logging
import tempfile
import subprocess

from .github import *


logger = logging.getLogger(__name__)


def release(repo_path, revision, cfg_root) -> dict:
    """
    """

    ret = dict()

    if revision:
        git_tag = revision
    else:
        cmd = ["git", "describe", "HEAD"]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, cwd=repo_path)
        git_tag = res.stdout.rstrip().decode()


    github_token = os.environ["GITHUB_TOKEN"]

    github_repo = get_remote(repo_path, cfg_root)

    tag2id, releases = get_repo_releases(github_repo)

    if git_tag in tag2id:
        release_id = tag2id[git_tag]
    else:
        release_id = create_release(github_repo, git_tag, github_token, cfg_root)

    ret["release_id"] = release_id

    ret["revision"] = git_tag

    tmpdir = "."
    local_path = download_default_release_asset(github_repo, release_id, github_token, tmpdir)
    ret["artifact_path"] = local_path

    if release_id in releases and releases[release_id]["assets"]:
        url = releases[release_id]["assets"][0]["browser_download_url"]
    else:
        url = upload_release_asset(github_repo, release_id, local_path, github_token)

    ret["artifact_url"] = url

    return ret


def postrelease(repo_path, cfg_root, release_meta, mirror_metas):

    github_token = os.environ["GITHUB_TOKEN"]

    github_repo = get_remote(repo_path, cfg_root)

    release_id = release_meta["release_id"]

    all_urls = list()
    for mirror, mirror_meta in mirror_metas.items():
        urls = mirror_meta["urls"]
        all_urls += urls

    update_release_with_mirror_urls(github_repo, release_id, github_token, all_urls)

    return {}
