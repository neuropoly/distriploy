#!/usr/bin/env python
# -*- coding: utf-8 vi:et

import sys, io, os, logging
import subprocess


logger = logging.getLogger(__name__)


def mirror(repo_path, config, release_meta):
    """
    """

    ret = dict()

    cmd = ["rsync", release_meta["artifact_path"], config["remote"]]
    subprocess.run(cmd)

    dirname, basename = os.path.split(release_meta["artifact_path"])
    ret["urls"] = ["/".join((config["public"], basename))]

    return ret
