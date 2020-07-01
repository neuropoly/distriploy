#!/usr/bin/env python
# -*- coding: utf-8 vi:et

import sys, io, os, logging
import argparse

from .distriploy import release


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
     default="INFO",
     help="logger level (eg. INFO, see Python logger docs)",
    )

    parser.add_argument("command",
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
     #datefmt="%Y%m%dT%H%M%S",
     #format="%(asctime)-15s %(name)s %(levelname)s %(message)s"
    )

    release_meta = release(args.repository, args.revision)

    mirror_metas = mirror(release_meta)

    #post_release(repo_path

if __name__ == "__main__":
    ret = main()
    raise SystemExit(ret)
