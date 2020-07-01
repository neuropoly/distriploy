#!/usr/bin/env python
# -*- coding: utf-8 vi:et

import sys, io, os, logging
import argparse
import json

from .distriploy import get_cfg, release, mirror, postrelease


logger = logging.getLogger(__name__)


def get_parser():
    parser = argparse.ArgumentParser(
     description="Create a release on one of the repositories within sct-data organization"
    )

    parser.add_argument("--repository",
     help="Repository to release (defaults to cwd)",
     default=".",
    )

    parser.add_argument("--revision",
     help="Revision to release (defaults to HEAD's git describe)",
    )

    parser.add_argument("--log-level",
     default="WARNING",
     help="logger level (eg. INFO, see Python logger docs)",
    )

    subparsers = parser.add_subparsers(
     help='the command; type "%s COMMAND -h" for command-specific help' % sys.argv[0],
     dest='command',
    )

    subp = subparsers.add_parser("release",
     help="Release",
    )

    return parser


def main(args_in=None):

    parser = get_parser()

    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except:
        pass

    args = parser.parse_args(args=args_in)

    logging.basicConfig(
     level=getattr(logging, args.log_level),
    )

    try:
        import coloredlogs
        coloredlogs.install(
         level=getattr(logging, args.log_level),
        )
    except ImportError:
        pass

    config = get_cfg(args.repository)

    release_meta = release(args.repository, args.revision, config)

    mirror_metas = mirror(args.repository, config, release_meta)

    postrelease_meta = postrelease(args.repository, config, release_meta, mirror_metas)

    root = json.dumps(postrelease_meta["urls"])
    print(root)

if __name__ == "__main__":
    ret = main()
    raise SystemExit(ret)
