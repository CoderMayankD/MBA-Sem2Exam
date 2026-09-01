"""Chunk a transcript, ground each chunk in retrieved slide/case-study material and matched
screenshots, then fold it into a running document one segment at a time (incremental merge).

Why incremental instead of map-then-reduce-all-at-once: a single reduce call scales its prompt
size with the whole lecture's segment count, which is exactly the kind of large-context call
that silently truncated to an empty response before `num_ctx` was fixed (see common.py). Merging
one small segment into a small running document at a time keeps every individual call's context
bounded regardless of lecture length, and persisting the running document after every step means
progress survives a crash instead of only living in memory until the very last call succeeds.

Why one combined prompt per segment instead of separate map + merge calls: the two-call version
worked but doubled wall-clock time for no real quality gain once the model can see the running
document, the raw transcript, and the fold-in instructions all at once — cut here specifically
because per-screenshot/per-segment turnaround time was too slow for practical use.
"""

from pathlib import Path

from .common import Ollama
from .retrieve import top_k

SKELETON = """## Quick Summary
None yet.

## Key Definitions
None yet.

## Worked Examples
None yet.

## Formulas & Rules
None yet.

## Tricky Logic & Traps
None yet.

## Exam Pointers
None yet.

## Sources
None yet.
"""

COMBINED_PROMPT = """You are maintaining ONE running exam-focused Markdown study note for an MBA \
lecture ("{title}", subject: {subject}), for an OPEN-BOOK exam that's calculation-heavy. You \
build it incrementally, one transcript segment at a time. Below is the document as it stands so \
far, followed by the next raw transcript segment to fold in.

Read the new transcript segment and UPDATE the document (do not start over):
- Add what's newly taught in this segment under the correct existing heading. Be concise — skip \
filler, small talk, repetition — but fully preserve any worked example or step-by-step problem \
(journal entries, ledger postings, ratio calculations, adjustments) in complete step-by-step form.
- For worked examples, capture the REASONING, not just the steps: why this item is an asset vs. \
expense, why debited not credited, why this formula applies and not a similar one, any mistake \
or counter-intuitive rule the instructor flagged. The exam is open-book, so formulas are already \
available — what actually trips students up is misjudging WHICH method applies and missing a \
"trick" in how a question is phrased. Capture that judgment explicitly whenever it's explained.
- `## Tricky Logic & Traps` is the most important section for this exam: capture every case where \
the instructor explains WHY a treatment applies, a common mistake, two similar things students \
confuse, or a counter-intuitive rule. Each point should be short, concrete, and self-contained — \
not a vague "be careful with X."
- Use "REFERENCE MATERIAL" only to check terminology/figures/structure against what the \
instructor actually said — don't copy it verbatim, don't add anything from it the instructor \
didn't cover. If it contributed anything, add its filename(s) to `## Sources` (deduplicated).
- Anything under "SCREENSHOT CONTENT" was physically shown on screen during this segment — it \
MUST be carried into the document in full (every row/column of any table), even if the \
instructor's narration only mentioned part of it. Put it in `## Worked Examples` if it's a \
calculation/journal entry/ledger, otherwise in `## Key Definitions`.
- Do NOT duplicate content already in the document. Do NOT drop or shorten anything already \
there — only add to it.
- Keep exactly these headings, in this order: `## Quick Summary`, `## Key Definitions`, \
`## Worked Examples`, `## Formulas & Rules`, `## Tricky Logic & Traps`, `## Exam Pointers`, \
`## Sources`. Replace "None yet." with real content once a section has any.
- Output ONLY the complete updated document — nothing else, no preamble.

--- DOCUMENT SO FAR ---
{running}

--- NEW TRANSCRIPT SEGMENT TO FOLD IN ---
{transcript}

--- REFERENCE MATERIAL (course slides / case studies) ---
{reference}

--- SCREENSHOT CONTENT CAPTURED DURING THIS SEGMENT ---
{screenshots}
"""


def chunk_transcript(segments: list[dict], target_minutes: float, pause_split_seconds: float) -> list[list[dict]]:
    if not segments:
        return []
    target = target_minutes * 60
    chunks, current = [], []
    chunk_start = segments[0]["start"]

    for i, seg in enumerate(segments):
        current.append(seg)
        duration = seg["end"] - chunk_start
        is_last = i == len(segments) - 1
        gap = (segments[i + 1]["start"] - seg["end"]) if not is_last else None

        if is_last:
            chunks.append(current)
            current = []
        elif duration >= target and gap is not None and gap >= pause_split_seconds:
            chunks.append(current)
            current = []
            chunk_start = segments[i + 1]["start"]
        elif duration >= target * 1.5:
            chunks.append(current)
            current = []
            chunk_start = segments[i + 1]["start"]

    return chunks


def _format_screenshots(shots: list[dict]) -> str:
    if not shots:
        return "(none)"
    return "\n\n".join(f"[{s['path'].split('/')[-1]}]\n{s['analysis']}" for s in shots)


def _format_reference(chunks: list[dict]) -> str:
    if not chunks:
        return "(none retrieved)"
    return "\n\n".join(f"(source: {c['source']} — {c['section']})\n{c['text']}" for c in chunks)


def generate_lecture_notes(
    segments: list[dict],
    screenshots: list[dict],
    doc_index: list[dict],
    ollama: Ollama,
    config: dict,
    title: str,
    subject: str,
    progress_dir: Path | None = None,
    on_progress=None,  # optional callback(running_text: str, done: bool) -> None, fired after every segment
) -> str:
    chunk_cfg = config["chunking"]
    retrieval_cfg = config["retrieval"]

    chunks = chunk_transcript(segments, chunk_cfg["chunk_target_minutes"], chunk_cfg["pause_split_seconds"])
    if not chunks:
        return "## Quick Summary\nNo speech detected in this recording.\n"

    if progress_dir:
        progress_dir.mkdir(parents=True, exist_ok=True)

    running = SKELETON
    for i, chunk in enumerate(chunks):
        c_start, c_end = chunk[0]["start"], chunk[-1]["end"]
        transcript_text = " ".join(s["text"] for s in chunk)
        chunk_shots = [s for s in screenshots if c_start - 5 <= s["timestamp_seconds"] <= c_end + 5]

        query_text = transcript_text[:3000]
        query_embedding = ollama.embed(query_text)
        reference_chunks = top_k(query_embedding, doc_index, retrieval_cfg["top_k"])

        prompt = COMBINED_PROMPT.format(
            title=title, subject=subject, running=running,
            transcript=transcript_text,
            reference=_format_reference(reference_chunks),
            screenshots=_format_screenshots(chunk_shots),
        )
        is_last = i == len(chunks) - 1
        new_running = ollama.generate(prompt, evict=is_last).strip()

        # "## Sources" is always the last heading the model should produce — if it's missing,
        # the response almost certainly got cut off (hit num_ctx or num_predict) rather than the
        # model choosing to omit it. Keep the previous good `running` instead of shipping a
        # silently-truncated document (this is exactly how the num_ctx bug slipped through once
        # already — see common.py/config.yaml history).
        if "## Sources" not in new_running:
            print(f"[notes] WARNING: segment {i + 1}/{len(chunks)} response looks truncated "
                  f"(no '## Sources' heading, {len(new_running)} chars) — keeping prior document, "
                  f"skipping this segment's content", flush=True)
        else:
            running = new_running

        if progress_dir:
            (progress_dir / "progress.md").write_text(running)
        if on_progress:
            on_progress(running, is_last)

        print(f"[notes] segment {i + 1}/{len(chunks)} folded in", flush=True)

    return running
