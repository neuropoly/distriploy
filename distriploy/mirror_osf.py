#!/usr/bin/env python
# -*- coding: utf-8 vi:et


from .osf import *


def mirror(repo_path, revision, config, release_meta):
    """
    """
    ret = dict()

    username = os.environ["OSF_USERNAME"]
    password = os.environ["OSF_PASSWORD"]

    url = upload_to_osf(
     config["project"],
     username, password,
     release_meta["artifact_path"],
     config["folder"],
     config.get("filename"),
    )

    ret["urls"] = [url]

    return ret
