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

    ret["release_id"] = release_id = create_release(github_repo, git_tag, github_token, cfg_root)

    tmpdir = "."
    local_path = download_default_release_asset(github_repo, release_id, github_token, tmpdir)
    ret["artifact_path"] = local_path
    url = upload_release_asset(github_repo, release_id, default_asset_path, github_token)
    ret["artifact_url"] = url

    return ret


def post_release(repo_path, revision, cfg_root, release_meta, mirror_metas):

    github_token = os.environ["GITHUB_TOKEN"]

    github_repo = get_remote(repo_path, cfg_root)

    release_id = release_meta["release_id"]

    all_urls = list()
    for mirror_meta in mirror_metas:
        urls = mirror_meta["urls"]
        all_urls += urls

    return update_release_with_mirror_urls(github_repo, release_id, github_token, all_urls)
