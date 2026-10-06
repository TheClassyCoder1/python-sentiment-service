import argparse
import json
import sys

from config import LEXICON_SOURCES
from core.lexicon_client import get_files_from_container, load_lexicon_file


def validate_source(source_name):
    """
    Ensuring that the specified source exists.
    :param source_name:
    :return:
    """
    if source_name:
        source = LEXICON_SOURCES.get(source_name)

        if not source:
            print(f"[-] No source found with name: {source_name}")
            sys.exit(1)

        return source


def main() -> None:
    parser = argparse.ArgumentParser(description="Lexicon management")
    sub = parser.add_subparsers(dest="command", required=True)

    sync = sub.add_parser("sync", help="List lexicon files of a source")
    sync.add_argument("--source", required=True)

    show = sub.add_parser("show", help="Print a local lexicon file")
    show.add_argument("path")

    args = parser.parse_args()
    if args.command == "sync":
        source = validate_source(args.source)
        files = get_files_from_container(source["container"])
        print(json.dumps(sorted(files), indent=2))
    elif args.command == "show":
        print(json.dumps(load_lexicon_file(args.path), indent=2))


if __name__ == "__main__":
    main()
