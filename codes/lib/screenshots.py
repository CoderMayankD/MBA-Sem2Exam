"""Scene-change screenshot extraction via ffmpeg, with timestamp-based de-duplication."""

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import imageio_ffmpeg

PTS_TIME_RE = re.compile(r"pts_time:([\d.]+)")


def _fmt_ts(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}-{m:02d}-{s:02d}"


def extract_screenshots(video_path: Path, out_dir: Path, scene_threshold: float, min_gap_seconds: float) -> list[dict]:
    """Returns [{path, timestamp_seconds}] for kept (de-duplicated) frames."""
    out_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = Path(tempfile.mkdtemp(prefix="lecture_shots_"))
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    cmd = [
        ffmpeg, "-y", "-i", str(video_path),
        "-vf", f"select='gt(scene,{scene_threshold})',showinfo",
        "-vsync", "vfr", "-qscale:v", "2",
        str(tmp_dir / "raw_%05d.png"),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    timestamps = [float(m.group(1)) for m in PTS_TIME_RE.finditer(proc.stderr)]

    raw_frames = sorted(tmp_dir.glob("raw_*.png"))
    kept = []
    last_kept_ts = -min_gap_seconds - 1
    for frame_path, ts in zip(raw_frames, timestamps):
        if ts - last_kept_ts < min_gap_seconds:
            continue
        dest = out_dir / f"shot_{_fmt_ts(ts)}.png"
        shutil.copy(frame_path, dest)
        kept.append({"path": dest, "timestamp_seconds": ts})
        last_kept_ts = ts

    shutil.rmtree(tmp_dir, ignore_errors=True)
    return kept
