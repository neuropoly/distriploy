#!/usr/bin/env python
# -*- coding: utf-8 vi:et

import sys, io, os, logging
import importlib

import yaml


logger = logging.getLogger(__name__)


def get_cfg(repo_path):

    config_path = os.path.join(repo_path, ".distriploy.yml")

    if not os.path.exists(config_path):
        raise FileNotFoundError(config_path)

    with io.open(config_path, "r", encoding="utf-8") as fi:
        data = fi.read()

    return yaml.safe_load(data)


def release(repo_path, revision, config):
    """
    Handle a release
    """

    cfg_release = config["release"]

    release_method_name = cfg_release["method"]

    try:
        mod = importlib.import_module(".release_{}".format(release_method_name), package=__package__)
        return mod.release(repo_path, revision, cfg_release)
    except Exception as e:
        logger.exception("Error importing %s: %s", release_method_name, e)
        raise


def mirror(repo_path, revision, config, release_meta):
    """
    Handle mirroring of a release.
    """
    mirror_metas = dict()

    cfg_mirrors = config["mirrors"]

    for mirror, info in cfg_mirrors.items():
        mirror_method_name = info["method"]

        try:
            mod = importlib.import_module(".mirror_{}".format(mirror_method_name), package=__package__)
        except Exception as e:
            logger.exception("Error importing %s: %s", mirror_method_name, e)
            continue

        try:
            mirror_meta = mod.mirror(repo_path, revision, info, release_meta)
            mirror_metas[mirror] = mirror_meta
        except Exception as e:
            logger.exception("Error running %s: %s", mirror_method_name, e)
            continue

    return mirror_metas


def postrelease(repo_path, revision, config, release_meta, mirror_metas):
    """
    """
    postrelease_meta = dict()

    return postrelease_meta
