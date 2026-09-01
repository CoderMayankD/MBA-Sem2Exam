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

    # Doc index per subject touched by this batch (cheap, cached — not worth redoing per lecture).
    doc_indexes = {}
    for subject in {r.subject for r in batch}:
        doc_indexes[subject] = build_or_update_index(subject, config)

    # Each recording is fully processed — transcribe, screenshots, vision, notes, write, push —
    # before moving to the next one. (Previously this ran phase-wise across the WHOLE batch:
    # transcribe everything, then screenshot everything, then vision-analyze everything, etc.,
    # which made sense back when vision and notes used two different Ollama models and swapping
    # between them per-lecture had a real cost. Now both use gemma4:12b — there's no swap cost
    # left to amortize — but the phase-wise structure meant NO lecture's notes file (or push)
    # appeared until vision analysis had finished for every recording in the batch, which could
    # be a long, silent wait. Per-lecture end-to-end fixes that: each lecture finishes and pushes
    # on its own before the next one starts.)
    ollama = Ollama(config)
    vision_max_tokens = config["models"].get("vision_max_tokens", 500)
    from lib.vision import analyze_screenshot

    for r in batch:
        print(f"=== {r.subject} / {r.title} ===", flush=True)

        # Free the LLM's VRAM before whisper's batched decode needs it — confirmed via a real
        # crash (CUDA OOM) that relying on the notes phase's own keep_alive:0 wasn't enough; the
        # 16GB card needs an explicit, *confirmed* handoff between whisper and gemma4:12b.
        ollama.unload_and_wait()
        segments = transcribe_video(r.path, r.subject, config)

        shots_dir = notes_dir(r.subject) / r.slug
        shots = extract_screenshots(
            r.path, shots_dir, config["screenshots"]["scene_threshold"], config["screenshots"]["min_gap_seconds"]
        )
        print(f"[screenshots] {r.title}: {len(shots)} candidate frame(s)")

        kept = []
        for i, shot in enumerate(shots, start=1):
            result = analyze_screenshot(shot["path"], ollama, max_tokens=vision_max_tokens)
            if result:
                result["timestamp_seconds"] = shot["timestamp_seconds"]
                kept.append(result)
            print(f"[vision] {r.title}: frame {i}/{len(shots)} ({'kept' if result else 'skip'})", flush=True)
        print(f"[vision] {r.title}: {len(kept)}/{len(shots)} frame(s) kept overall")

        # Notes built incrementally (small running doc + one segment at a time, see notes.py),
        # persisted to Notes/.cache/progress/<slug>/ after every step, and the real
        # Notes/<slug>.md file is rewritten after every segment too (not just at the end) so
        # it's visible and updating live if you have it open.
        print(f"[notes] generating for {r.title}")
        progress_dir = cache_dir(r.subject) / "progress" / r.slug

        def on_progress(running_text, done, r=r):
            write_notes_file(r, segments, running_text, done=done)

        body = generate_lecture_notes(
            segments, kept, doc_indexes[r.subject],
            ollama, config, r.title, r.subject, progress_dir=progress_dir, on_progress=on_progress,
        )
        out_path = write_notes_file(r, segments, body)
        print(f"[notes] wrote {out_path.relative_to(REPO_ROOT)}")

        rebuild_master(config)
        commit_and_push(
            ["codes", ".gitignore", config["paths"]["master_file"], f"{r.subject}/Notes"],
            f"Notes: {r.subject} — {r.title}",
        )


if __name__ == "__main__":
    main()
