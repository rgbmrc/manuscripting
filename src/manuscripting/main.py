import argparse
import re
from pathlib import Path
from .mauscripting import enc, sub, bib


def redirect(callback, **args):
    return callback(**args)


def main():
    proj = Path.cwd().name
    opts = dict(fromfile_prefix_chars="@")
    parser = argparse.ArgumentParser(**opts)
    subparsers = parser.add_subparsers()
    subparsers.required = True

    p = subparsers.add_parser("enc", help="change text encoding", **opts)
    p.set_defaults(callback=enc)
    p.add_argument("encoding", choices=("ascii", "unicode"), help="encoding")
    p.add_argument("files", nargs="+", help="files to encode")

    p = subparsers.add_parser("bib", help="import a bibliography", **opts)
    p.set_defaults(callback=bib)
    p.add_argument("source", help="source bib file")
    p.add_argument(
        "dest",
        nargs="?",
        help="destination bib file [default: same as source file name]",
    )
    p.add_argument(
        "-o",
        "--omit",
        nargs="*",
        help="fields to be omitted",
    )
    p.add_argument(
        "-j",
        "--only-journal",
        action="store_true",
        help="omit eprint field for published papers",
    )
    p.add_argument(
        "-a",
        "--max-authors",
        type=int,
        help="maximum number of authors, if more 'et al' is used",
    )

    p = subparsers.add_parser("sub", help="prepare submission", **opts)
    p.set_defaults(callback=sub)
    p.add_argument("subname", help="submission name")
    p.add_argument(
        "projname",
        nargs="?",
        default=proj,
        help="project name [default: %(default)s]",
    )
    p.add_argument(
        "-n",
        "--no-build",
        action="store_true",
        help="do not build the project beforehand",
    )
    p.add_argument(
        "--exclude",
        action="extend",
        nargs="*",
        help="files to exclude",
    )
    p.add_argument(
        "-b",
        "--bibliography",
        action="store_true",
        help="embed referenced bib entries",
    )
    p.add_argument(
        "-i",
        "--input",
        action="store_true",
        help="embed inputted tex files",
    )

    redirect(**vars(parser.parse_args()))
