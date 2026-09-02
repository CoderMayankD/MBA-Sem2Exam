#!/usr/bin/env python3
"""Build/refresh the unified hybrid-search index across all subjects (or one, if given).
Re-run whenever new lectures are processed — already-embedded chunks are reused (keyed by
subject+source_type+label+text), so this is cheap after the first full build.

Usage: ../.venv/bin/python3 build_search_index.py [Subject name]
"""

import sys

from lib.common import load_config
from lib.search_index import build_index


def main():
    config = load_config()
    subjects = [sys.argv[1]] if len(sys.argv) > 1 else None
    build_index(config, subjects)


if __name__ == "__main__":
    main()
