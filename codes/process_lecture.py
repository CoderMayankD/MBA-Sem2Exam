#!/usr/bin/env python3
"""CLI entrypoint for the lecture-video -> Markdown-notes pipeline.

Usage:
  python process_lecture.py --subject "Managerial Accounting" --all
  python process_lecture.py "Managerial Accounting/shared/Recordings/some-file.mp4"
  python process_lecture.py --subject "Managerial Accounting" --all --force
  python process_lecture.py --subject "Managerial Accounting" --all --dry-run
  python process_lecture.py --rebuild-doc-index --subject "Managerial Accounting"
"""

import argparse
import datetime
import sys
from pathlib import Path

from lib.common import Ollama, REPO_ROOT, cache_dir, load_config, notes_dir
from lib.discover import Recording, find_recordings
from lib.docs_index import build_or_update_index
from lib.git_sync import commit_and_push
from lib.master import rebuild_master
from lib.notes import generate_lecture_notes
from lib.screenshots import extract_screenshots
from lib.transcribe import transcribe_video


def resolve_batch(args, config) -> list[Recording]:
    if args.video:
        video_path = Path(args.video).resolve()
        for subject in config["subjects"]:
            for r in find_recordings(subject):
                if r.path.resolve() == video_path:
                    return [r]
        print(f"ERROR: {video_path} is not under any configured subject's shared/Recordings/ folder.")
        sys.exit(1)

    if not args.subject:
        print("ERROR: pass either a video path or --subject <name> --all")
        sys.exit(1)
    if args.subject not in config["subjects"]:
        print(f"ERROR: '{args.subject}' is not in config.yaml's subjects list: {config['subjects']}")
        sys.exit(1)

    recordings = find_recordings(args.subject)
    if not args.force:
        n_dir = notes_dir(args.subject)
        recordings = [r for r in recordings if not _notes_are_done(n_dir / f"{r.slug}.md")]
    return recordings


def _notes_are_done(path: Path) -> bool:
    """A notes file only counts as done if its frontmatter says so — an in-progress file (partial,
    written live segment-by-segment) has the same filename but must NOT be treated as finished,
    otherwise a restart (crash, reboot, kill) would permanently skip a lecture that never actually
    completed. This is what makes --all resumable after a system restart."""
    if not path.exists():
        return False
    head = path.read_text()[:400]
    return "status: done" in head


def write_notes_file(recording: Recording, segments: list[dict], body: str, done: bool = True) -> Path:
    """Writes the real Notes/<slug>.md file. Called after every segment while generating (done=False,
    so the file the user has open updates live) and once more at the end (done=True)."""
    n_dir = notes_dir(recording.subject)
    out_path = n_dir / f"{recording.slug}.md"
    duration_min = int(segments[-1]["end"] // 60) if segments else 0
    frontmatter = (
        "---\n"
        f"title: {recording.title}\n"
        f"subject: {recording.subject}\n"
        f"source_video: {recording.path.name}\n"
        f"duration_minutes: {duration_min}\n"
        f"processed_on: {datetime.date.today().isoformat()}\n"
        f"status: {'done' if done else 'in-progress — still generating, will keep updating'}\n"
        "---\n\n"
    )
    out_path.write_text(f"{frontmatter}# {recording.title}\n\n{body}\n")
    return out_path


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("video", nargs="?", help="Path to a single video file to process")
    parser.add_argument("--subject", help="Subject folder name (must match config.yaml)")
    parser.add_argument("--all", action="store_true", help="Process every not-yet-processed recording for --subject")
    parser.add_argument("--force", action="store_true", help="Reprocess even if notes already exist")
    parser.add_argument("--dry-run", action="store_true", help="Print the plan without calling any model")
    parser.add_argument("--rebuild-doc-index", action="store_true", help="Force re-embedding of shared/ documents")
    args = parser.parse_args()

    config = load_config()

    subjects_touched = [args.subject] if args.subject else config["subjects"]
    if args.rebuild_doc_index:
        for subject in subjects_touched:
            build_or_update_index(subject, config, force=True)
        if not args.video and not args.all:
            return

    batch = resolve_batch(args, config)
    if not batch:
        print("Nothing to process (all recordings already have notes — use --force to redo).")
        rebuild_master(config)
        return

    print(f"Batch: {len(batch)} recording(s)")
    for r in batch:
        print(f"  {r.subject} / {r.title} <- {r.path.name}")

    if args.dry_run:
        print("(dry run, stopping here)")
        return

    # Phase 0: make sure each involved subject's document index is current (cheap, cached).
    doc_indexes = {}
    for subject in {r.subject for r in batch}:
        doc_indexes[subject] = build_or_update_index(subject, config)

    # Phase 1: transcribe every video (one whisper model instance, reused across the batch).
    transcripts = {}
    for r in batch:
        transcripts[r.slug] = transcribe_video(r.path, r.subject, config)

    # Phase 2: extract screenshots for every video (ffmpeg only, no GPU model contention).
    screenshots = {}
    for r in batch:
        shots_dir = notes_dir(r.subject) / r.slug
        screenshots[r.slug] = extract_screenshots(
            r.path, shots_dir, config["screenshots"]["scene_threshold"], config["screenshots"]["min_gap_seconds"]
        )
        print(f"[screenshots] {r.title}: {len(screenshots[r.slug])} candidate frame(s)")

    # Phase 3: vision-analyze every screenshot (gemma4:12b loaded once, stays resident).
    ollama = Ollama(config)
    analyzed_shots = {}
    for r in batch:
        from lib.vision import analyze_screenshot

        kept = []
        total = len(screenshots[r.slug])
        vision_max_tokens = config["models"].get("vision_max_tokens", 500)
        for i, shot in enumerate(screenshots[r.slug], start=1):
            result = analyze_screenshot(shot["path"], ollama, max_tokens=vision_max_tokens)
            if result:
                result["timestamp_seconds"] = shot["timestamp_seconds"]
                kept.append(result)
            print(f"[vision] {r.title}: frame {i}/{total} ({'kept' if result else 'skip'})", flush=True)
        analyzed_shots[r.slug] = kept
        print(f"[vision] {r.title}: {len(kept)}/{total} frame(s) kept overall")

    # Phase 4: generate notes per video (same gemma4:12b session, no model swap needed).
    # Notes are built incrementally (small running doc + one segment at a time, see notes.py)
    # and persisted to Notes/.cache/progress/<slug>/ after every step, so nothing depends on one
    # big context window and progress survives even if a later segment fails. The real
    # Notes/<slug>.md file is also rewritten after every segment (not just at the end) so it's
    # visible and updating live if the user has it open.
    for r in batch:
        print(f"[notes] generating for {r.title}")
        progress_dir = cache_dir(r.subject) / "progress" / r.slug

        def on_progress(running_text, done, r=r):
            write_notes_file(r, transcripts[r.slug], running_text, done=done)

        body = generate_lecture_notes(
            transcripts[r.slug], analyzed_shots[r.slug], doc_indexes[r.subject],
            ollama, config, r.title, r.subject, progress_dir=progress_dir, on_progress=on_progress,
        )
        out_path = write_notes_file(r, transcripts[r.slug], body)
        print(f"[notes] wrote {out_path.relative_to(REPO_ROOT)}")

        # Rebuild + push after EVERY lecture (not just once at the end) so remote progress is
        # checkable lecture-by-lecture, per explicit user request.
        rebuild_master(config)
        commit_and_push(
            ["codes", ".gitignore", config["paths"]["master_file"], f"{r.subject}/Notes"],
            f"Notes: {r.subject} — {r.title}",
        )


if __name__ == "__main__":
    main()
