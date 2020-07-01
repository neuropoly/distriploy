#!/usr/bin/env python
# -*- coding: utf-8 vi:et

import sys, io, os, logging
import subprocess
import base64
import urllib.parse, urllib.request, urllib.error
import json

logger = logging.getLogger(__name__)


def mirror(repo_path, config, release_meta):
    """
    """

    ret = dict()

    username = os.environ["ACADEMICTORRENTS_USERNAME"]
    password = os.environ["ACADEMICTORRENTS_PASSWORD"]

    dirname, basename = os.path.split(release_meta["artifact_path"])

    torrent = f"{basename}.torrent"

    logger.info("Create torrent %s", torrent)

    cmd = ["ctorrent",
     "-t",
     "-u", "https://academictorrents.com/announce.php",
     "-s", torrent, basename,
    ]

    subprocess.run(cmd, cwd=dirname, stdout=subprocess.PIPE)

    logger.info("Register torrent %s", torrent)

    torrent = os.path.join(dirname, torrent)

    with io.open(torrent, "rb") as fi:
        data = fi.read()

    b64_torrent = base64.b64encode(data).decode()

    post_params = config["params"].copy()
    post_params["name"] = "{} (revision: {})".format(post_params["name"], release_meta["revision"])
    post_params["uid"] = username
    post_params["pass"] = password
    post_params["file"] = b64_torrent
    post_params["urllist"] = ", ".join([release_meta["artifact_url"]])
    logger.info("post params: %s", post_params)

    data = urllib.parse.urlencode(post_params).encode('utf-8')

    logger.info("data: %s", data.decode("utf-8"))

    url = "https://academictorrents.com/apiv2/entry"
    req = urllib.request.Request(url, method="POST", data=data)

    with urllib.request.urlopen(req) as resp:
        if resp.getcode() != 200:
            msg = "Bad response: {} / {}".format(resp.getcode(), resp.read())
            raise RuntimeError(msg)
        ret = json.loads(resp.read().decode("utf-8"))
        logger.info("academictorrent says: %s", ret)

        infohash = ret["url"].rsplit("/", 1)[-1]
        ret["infohash"] = infohash
        ret["urls"] = [
         f"https://academictorrents.com/download/{infohash}.torrent",
         f"magnet:?xt=urn:btih:{infohash}&tr=http%3A%2F%2Facademictorrents.com%2Fannounce.php&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969",
        ]

    return ret
