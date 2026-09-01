"""Commit + push one lecture's notes to GitHub as soon as it's done, so progress is checkable
remotely without waiting for the whole batch to finish. Never touches video/large media —
.gitignore already excludes those; this only ever stages small, generated/text content.
"""

import subprocess

from .common import REPO_ROOT


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=REPO_ROOT, capture_output=True, text=True)


def commit_and_push(paths: list[str], message: str) -> None:
    """paths: repo-relative paths/globs to stage (e.g. a subject's Notes/ dir, MASTER.md).
    Never raises — a git/network hiccup shouldn't take down the processing run; it just prints
    a warning and the next lecture's commit will pick up any leftover unstaged changes too."""
    try:
        add = _run(["git", "add", "--"] + paths)
        if add.returncode != 0:
            print(f"[git] WARNING: git add failed: {add.stderr.strip()}")
            return

        staged = _run(["git", "diff", "--cached", "--quiet"])
        if staged.returncode == 0:
            return  # nothing to commit (e.g. re-running an already-pushed lecture)

        commit = _run(["git", "commit", "-m", message])
        if commit.returncode != 0:
            print(f"[git] WARNING: git commit failed: {commit.stderr.strip()}")
            return

        push = _run(["git", "push", "origin", "HEAD"])
        if push.returncode != 0:
            print(f"[git] WARNING: git push failed (commit is saved locally, will retry next lecture): {push.stderr.strip()}")
            return

        print(f"[git] pushed: {message}")
    except Exception as e:
        print(f"[git] WARNING: git sync raised {e!r}, continuing without pushing")
