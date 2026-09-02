#!/usr/bin/env python3
"""Build Managerial Accounting/Practice-Questions.md:
  Part 1 — one quick topic+logic recap and a practice Q&A per lecture, generated from that
           lecture's own notes (short, exam-style, tests the trickiest concept covered).
  Part 2 — the instructor's own existing question banks from shared/, surfaced as-is (no LLM
           regeneration — they're already correct, faster and safer to just extract verbatim).

Usage: ../.venv/bin/python3 generate_practice_questions.py
"""

from pathlib import Path

from lib.common import Ollama, REPO_ROOT, load_config, notes_dir, subject_dir
from lib.discover import find_recordings
from lib.docs_index import _extract_docx, _extract_pdf, _extract_xlsx
from lib.git_sync import commit_and_push

SUBJECT = "Managerial Accounting"

PROMPT = """Below are condensed study notes for one lecture from an MBA Managerial Accounting \
course (open-book exam). Produce EXACTLY this, short and to the point — no extra commentary:

STRICT RULE: use ONLY the concepts, rules, terminology, and worked-example numbers/scenarios \
that actually appear in these notes below. Do not introduce any accounting rule, classification, \
or method the notes don't mention, even if it's standard textbook knowledge — if it's not in \
these notes, it doesn't exist for this exercise. The question should either reuse a scenario \
from the notes' own Worked Examples (changing at most the numbers) or directly test a specific \
point from Tricky Logic & Traps — never a new scenario built from outside knowledge.

**Topic:** <one line naming the topic>
**Logic:** <2-3 sentences explaining the core logic/rule a student needs to apply — the "why", \
not just the "what" — quoting/paraphrasing only what these notes actually say>
**Practice Question:** <one exam-style question testing the trickiest/most-confused concept in \
these notes — a calculation or classification judgment call, not a pure definition recall>
**Solution:** <short step-by-step solution/answer, derived only from the logic given in these notes>
**Why:** <one sentence on the reasoning/trap this question is testing>

--- LECTURE NOTES ---
{notes}
"""

EXISTING_DOCS = [
    "Financial_Ratio_Analysis_20_Practice_Questions_with_Solutions.docx",
    "Standard_Costing_Variance_Questions_with_Solutions.docx",
    "PV ratio practice question.docx",
    "Advanced_Financial_Ratio_Analysis_20_Classroom_Problems_Solutions.docx",
    "Ribbon an' Bows Case Study.pdf",
    "Ribbons and bows-Solution.xlsx",
]


def extract_existing(shared_dir: Path) -> str:
    out = []
    for fname in EXISTING_DOCS:
        path = shared_dir / fname
        if not path.exists():
            continue
        ext = path.suffix.lower()
        extractor = {".docx": _extract_docx, ".pdf": _extract_pdf, ".xlsx": _extract_xlsx}[ext]
        try:
            sections = extractor(path)
        except Exception as e:
            out.append(f"### {fname}\n\n(could not extract: {e})\n")
            continue
        text = "\n\n".join(t for _, t in sections).strip()
        if not text or len(text) < 50:
            out.append(f"### {fname}\n\n(no extractable text — likely a scanned/image PDF; open the original file directly)\n")
            continue
        out.append(f"### {fname}\n\n{text}\n")
    return "\n".join(out)


def main():
    config = load_config()
    ollama = Ollama(config)
    n_dir = notes_dir(SUBJECT)
    recordings = find_recordings(SUBJECT)

    print(f"Generating per-lecture practice Q&A for {len(recordings)} lectures...")
    lecture_sections = []
    for r in recordings:
        notes_path = n_dir / f"{r.slug}.md"
        if not notes_path.exists():
            continue
        notes_text = notes_path.read_text()
        prompt = PROMPT.format(notes=notes_text[:6000])
        result = ollama.generate(prompt, evict=False)
        lecture_sections.append(f"## Lecture {r.lecture_num:02d} ({r.date_str})\n\n{result.strip()}\n")
        print(f"  Lecture {r.lecture_num:02d} done", flush=True)
    ollama.unload_and_wait()

    print("Extracting existing question banks from shared/...")
    existing = extract_existing(subject_dir(SUBJECT) / "shared")

    out_path = subject_dir(SUBJECT) / "Practice-Questions.md"
    content = (
        f"# {SUBJECT} — Practice Questions\n\n"
        "_Part 1 is auto-generated per lecture (quick recap + one exam-style question testing "
        "the trickiest concept covered). Part 2 is extracted directly from the course's own "
        "question banks — verbatim, not LLM-regenerated, so treat those as authoritative._\n\n"
        "## Part 1: Lecture-by-Lecture Quick Practice\n\n"
        + "\n".join(lecture_sections)
        + "\n## Part 2: Existing Course Question Banks (from shared materials)\n\n"
        + existing
    )
    out_path.write_text(content)
    print(f"Wrote {out_path.relative_to(REPO_ROOT)}")

    commit_and_push(["codes", f"{SUBJECT}/Practice-Questions.md"], f"Add practice questions: {SUBJECT}")


if __name__ == "__main__":
    main()
