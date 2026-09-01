#!/usr/bin/env python3
"""Quick progress check across all subjects — run anytime, doesn't touch the running pipeline.

Usage: ../.venv/bin/python3 progress.py
"""

from lib.common import REPO_ROOT, load_config, notes_dir
from lib.discover import find_recordings


def _bar(done: int, total: int, width: int = 30) -> str:
    if total == 0:
        return "[" + " " * width + "]  (no recordings found)"
    filled = round(width * done / total)
    return f"[{'#' * filled}{'-' * (width - filled)}] {done}/{total} ({100 * done // total}%)"


def _current_status(path) -> str | None:
    if not path.exists():
        return None
    head = path.read_text()[:400]
    if "status: done" in head:
        return "done"
    if "status: in-progress" in head:
        return "in-progress"
    return "unknown"


def main():
    config = load_config()
    print()
    grand_done, grand_total = 0, 0
    for subject in config["subjects"]:
        recordings = find_recordings(subject)
        n_dir = notes_dir(subject)
        done = sum(1 for r in recordings if _current_status(n_dir / f"{r.slug}.md") == "done")
        in_progress = [r for r in recordings if _current_status(n_dir / f"{r.slug}.md") == "in-progress"]
        total = len(recordings)
        grand_done += done
        grand_total += total
        print(f"{subject}")
        print(f"  {_bar(done, total)}")
        if in_progress:
            print(f"  currently processing: {in_progress[0].title}")
        print()

    print("Overall")
    print(f"  {_bar(grand_done, grand_total)}")
    print()


if __name__ == "__main__":
    main()
