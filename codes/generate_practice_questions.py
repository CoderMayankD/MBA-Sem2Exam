#!/usr/bin/env python3
"""Build <Subject>/Practice-Questions.md:
  Part 1 — one quick topic+logic recap and a practice Q&A per lecture, generated from that
           lecture's own notes (short, exam-style, tests the trickiest concept covered).
  Part 2 — the instructor's own existing question/case materials from shared/, surfaced as-is
           (no LLM regeneration — they're already correct, faster and safer to just extract
           verbatim). Auto-discovered by filename keywords, not a hardcoded list per subject.

Usage: ../.venv/bin/python3 generate_practice_questions.py "<Subject name>"
"""

import sys
from pathlib import Path

from lib.common import Ollama, REPO_ROOT, load_config, notes_dir, subject_dir
from lib.discover import find_recordings
from lib.docs_index import _extract_docx, _extract_pdf, _extract_pptx, _extract_xlsx
from lib.git_sync import commit_and_push

PROMPT = """Below are condensed study notes for one lecture from an MBA {subject} course \
(open-book exam). Produce EXACTLY this, short and to the point — no extra commentary:

STRICT RULE: use ONLY the concepts, rules, terminology, and scenarios that actually appear in \
these notes below. Do not introduce any rule, framework, or method the notes don't mention, even \
if it's standard textbook knowledge — if it's not in these notes, it doesn't exist for this \
exercise. The question should either reuse a scenario from the notes' own Worked Examples \
(changing at most the numbers/names) or directly test a specific point from Tricky Logic & Traps \
— never a new scenario built from outside knowledge.

**Topic:** <one line naming the topic>
**Logic:** <2-3 sentences explaining the core logic/rule a student needs to apply — the "why", \
not just the "what" — quoting/paraphrasing only what these notes actually say>
**Practice Question:** <one exam-style question testing the trickiest/most-confused concept in \
these notes — a judgment call or applied scenario, not a pure definition recall>
**Solution:** <short step-by-step solution/answer, derived only from the logic given in these notes>
**Why:** <one sentence on the reasoning/trap this question is testing>

--- LECTURE NOTES ---
{notes}
"""

KEYWORDS = ["question", "practice", "problem", "solution", "case study", "sample paper", "midsem"]

EXTRACTORS = {".docx": _extract_docx, ".pdf": _extract_pdf, ".xlsx": _extract_xlsx, ".pptx": _extract_pptx}


def find_existing_materials(shared_dir: Path) -> list[Path]:
    found = []
    for path in shared_dir.glob("*"):
        if path.suffix.lower() not in EXTRACTORS:
            continue
        name_lower = path.name.lower()
        if any(kw in name_lower for kw in KEYWORDS):
            found.append(path)
    return sorted(found)


def extract_existing(shared_dir: Path) -> str:
    out = []
    for path in find_existing_materials(shared_dir):
        extractor = EXTRACTORS[path.suffix.lower()]
        try:
            sections = extractor(path)
        except Exception as e:
            out.append(f"### {path.name}\n\n(could not extract: {e})\n")
            continue
        text = "\n\n".join(t for _, t in sections).strip()
        if not text or len(text) < 50:
            out.append(f"### {path.name}\n\n(no extractable text — likely a scanned/image file; open the original directly)\n")
            continue
        out.append(f"### {path.name}\n\n{text}\n")
    return "\n".join(out)


def main():
    if len(sys.argv) < 2:
        print("Usage: generate_practice_questions.py <Subject name>")
        sys.exit(1)
    subject = sys.argv[1]

    config = load_config()
    ollama = Ollama(config)
    n_dir = notes_dir(subject)
    recordings = find_recordings(subject)

    print(f"Generating per-lecture practice Q&A for {len(recordings)} lectures...")
    lecture_sections = []
    for r in recordings:
        notes_path = n_dir / f"{r.slug}.md"
        if not notes_path.exists():
            continue
        notes_text = notes_path.read_text()
        prompt = PROMPT.format(subject=subject, notes=notes_text[:6000])
        result = ollama.generate(prompt, evict=False)
        lecture_sections.append(f"## Lecture {r.lecture_num:02d} ({r.date_str})\n\n{result.strip()}\n")
        print(f"  Lecture {r.lecture_num:02d} done", flush=True)
    ollama.unload_and_wait()

    print("Extracting existing question/case materials from shared/...")
    shared_dir = subject_dir(subject) / "shared"
    existing_files = find_existing_materials(shared_dir)
    print(f"  found: {[p.name for p in existing_files]}")
    existing = extract_existing(shared_dir)

    out_path = subject_dir(subject) / "Practice-Questions.md"
    content = (
        f"# {subject} — Practice Questions\n\n"
        "_Part 1 is auto-generated per lecture (quick recap + one exam-style question testing "
        "the trickiest concept covered). Part 2 is extracted directly from the course's own "
        "question/case materials — verbatim, not LLM-regenerated, so treat those as authoritative._\n\n"
        "## Part 1: Lecture-by-Lecture Quick Practice\n\n"
        + "\n".join(lecture_sections)
        + "\n## Part 2: Existing Course Materials (from shared/)\n\n"
        + (existing if existing else "_No question/case-study/sample-paper files found in shared/._\n")
    )
    out_path.write_text(content)
    print(f"Wrote {out_path.relative_to(REPO_ROOT)}")

    commit_and_push(["codes", f"{subject}/Practice-Questions.md"], f"Add practice questions: {subject}")


if __name__ == "__main__":
    main()
