"""Find lecture recordings for a subject and assign chronological lecture numbers."""

import re
from dataclasses import dataclass
from pathlib import Path

from .common import slugify, subject_dir

DATE_RE = re.compile(r"(20\d{2})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})")


@dataclass
class Recording:
    subject: str
    path: Path
    lecture_num: int
    date_str: str  # e.g. 2026-04-26
    title: str
    slug: str


def _parse_date(filename: str) -> str | None:
    m = DATE_RE.search(filename)
    if not m:
        return None
    y, mo, d, h, mi, s = m.groups()
    return f"{y}-{mo}-{d} {h}:{mi}:{s}"


def find_recordings(subject: str) -> list[Recording]:
    """Recurse into shared/Recordings/**, sort chronologically by embedded date/time,
    fall back to filesystem mtime for files with no parseable date, and number 01, 02, ...
    """
    root = subject_dir(subject) / "shared" / "Recordings"
    if not root.exists():
        return []

    videos = sorted(root.rglob("*.mp4"))
    dated = []
    for v in videos:
        date_str = _parse_date(v.name)
        if date_str is None:
            date_str = None
        dated.append((v, date_str))

    def sort_key(item):
        v, date_str = item
        if date_str:
            return (0, date_str)
        return (1, v.stat().st_mtime)

    dated.sort(key=sort_key)

    recordings = []
    for i, (v, date_str) in enumerate(dated, start=1):
        display_date = date_str.split(" ")[0] if date_str else "unknown-date"
        title = f"Lecture {i:02d} ({display_date})"
        recordings.append(
            Recording(
                subject=subject,
                path=v,
                lecture_num=i,
                date_str=display_date,
                title=title,
                slug=f"{i:02d}-{slugify(subject)}-lecture-{i:02d}",
            )
        )
    return recordings
