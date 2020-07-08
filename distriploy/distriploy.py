#!/usr/bin/env python
# -*- coding: utf-8 vi:et

import sys, io, os, logging
import importlib

import yaml


logger = logging.getLogger(__name__)


def get_cfg(repo_path):
    """
    Parse distriploy config
    """

    config_path = os.path.join(repo_path, ".distriploy.yml")

    if not os.path.exists(config_path):
        raise FileNotFoundError(config_path)

    with io.open(config_path, "r", encoding="utf-8") as fi:
        data = fi.read()

    return yaml.safe_load(data)


def get_module(name, module_type):
    """
    Get a plug-in module
    """

    modname = ".{}_{}".format(module_type, name)
    try:
        return importlib.import_module(modname, package=__package__)
    except ModuleNotFoundError:
        pass

    modname = "distriploy_{}_{}".format(module_type, name)
    try:
        return importlib.import_module(modname)
    except ModuleNotFoundError:
        raise


def release(repo_path, revision, config):
    """
    Handle a release
    """

    cfg_release = config["release"]

    release_method_name = cfg_release["method"]

    mod = get_module(release_method_name, "release")

    return mod.release(repo_path, revision, cfg_release)


def mirror(repo_path, config, release_meta):
    """
    Handle mirroring of a release.
    """
    mirror_metas = dict()

    cfg_mirrors = config["mirrors"]

    for mirror, info in cfg_mirrors.items():
        mirror_method_name = info["method"]

        try:
            mod = get_module(mirror_method_name, "mirror")
        except ModuleNotFoundError as e:
            logger.exception("Mirroring plug-in %s (%s) not found, skipping",
             mirror, mirror_method_name)
            continue
        except Exception as e:
            logger.exception("Error importing mirroring plug-in %s (%s): %s",
             mirror, mirror_method_name, e)
            continue

        try:
            mirror_meta = mod.mirror(repo_path, info, release_meta)
            mirror_metas[mirror] = mirror_meta
        except Exception as e:
            logger.exception("Error running %s: %s", mirror_method_name, e)
            continue

    return mirror_metas


def postrelease(repo_path, config, release_meta, mirror_metas):
    """
    Call postrelease() in release module.
    """

    postrelease_meta = dict()

    all_urls = list()
    for mirror, mirror_meta in mirror_metas.items():
        urls = mirror_meta["urls"]
        all_urls += urls

    if all_urls:
        logger.info("All URLs:")
        for url in all_urls:
            logger.info("- %s", url)

    cfg_release = config["release"]

    cfg_postrelease = config["postrelease"]

    release_method_name = cfg_release["method"]

    try:
        mod = get_module(release_method_name, "release")
    except Exception as e:
        logger.exception("Error importing %s: %s", release_method_name, e)
        raise

    postrelease = getattr(mod, "postrelease", None)
    if postrelease is not None:
        postrelease_meta = postrelease(repo_path, cfg_postrelease, release_meta, mirror_metas)


    postrelease_meta["urls"] = all_urls

    if "artifact_url" in release_meta:
       postrelease_meta["urls"] = [release_meta["artifact_url"]] + all_urls

    return postrelease_meta
