"""Build one unified, hybrid-searchable index across every subject: the shared/ course
documents (reusing the already-embedded doc_index), the generated lecture notes (chunked by
heading), and the raw lecture transcripts (chunked into ~75s windows). Each entry gets an
embedding (for semantic search) and is later also fed to a BM25 index (for lexical search) —
see search_server.py for how the two are combined.
"""

from pathlib import Path

from .common import Ollama, cache_dir, file_hash, notes_dir, read_json, subject_dir, write_json
from .discover import find_recordings
from .notes import chunk_transcript

INDEX_PATH = Path(__file__).resolve().parents[1] / ".cache" / "search_index.json"


def _notes_chunks(subject: str) -> list[dict]:
    chunks = []
    n_dir = notes_dir(subject)
    for md_path in sorted(n_dir.glob("*.md")):
        text = md_path.read_text()
        # split on '## ' headings, skip the frontmatter block above the first one
        body = text.split("\n## ", 1)
        if len(body) < 2:
            continue
        title_line = text.split("\n# ", 1)
        lecture_title = title_line[1].split("\n", 1)[0].strip() if len(title_line) > 1 else md_path.stem
        sections = ("## " + body[1]).split("\n## ")
        for sec in sections:
            heading, _, content = sec.partition("\n")
            content = content.strip()
            if not content or content == "None yet." or len(content) < 40:
                continue
            chunks.append({
                "subject": subject,
                "source_type": "notes",
                "label": f"{lecture_title} — {heading.strip('# ').strip()}",
                "text": content[:4000],
                "link": f"{subject}/Notes/{md_path.stem}.md",
            })
    return chunks


def _transcript_chunks(subject: str) -> list[dict]:
    chunks = []
    for r in find_recordings(subject):
        cache_path = cache_dir(subject) / "transcripts" / f"{file_hash(r.path)}.json"
        data = read_json(cache_path)
        if not data or not data.get("segments"):
            continue
        windows = chunk_transcript(data["segments"], target_minutes=1.25, pause_split_seconds=1.5)
        for w in windows:
            text = " ".join(s["text"] for s in w).strip()
            if len(text) < 40:
                continue
            start_min = w[0]["start"] / 60
            chunks.append({
                "subject": subject,
                "source_type": "transcript",
                "label": f"{r.title} @ {start_min:.1f}min",
                "text": text[:2000],
                "link": f"{subject}/Notes/{r.slug}.md",
            })
    return chunks


def _shared_doc_chunks(subject: str) -> list[dict]:
    doc_index_path = cache_dir(subject) / "doc_index.json"
    data = read_json(doc_index_path, default={"chunks": []})
    chunks = []
    for c in data["chunks"]:
        chunks.append({
            "subject": subject,
            "source_type": "shared_doc",
            "label": f"{c['source']} — {c['section']}",
            "text": c["text"],
            "link": f"{subject}/shared/{c['source']}",
            "embedding": c["embedding"],  # already computed, reuse — don't re-embed
        })
    return chunks


def build_index(config: dict, subjects: list[str] | None = None) -> list[dict]:
    subjects = subjects or config["subjects"]
    ollama = Ollama(config)

    existing = read_json(INDEX_PATH, default=[])
    existing_by_key = {(e["subject"], e["source_type"], e["label"]): e for e in existing}

    all_entries = []
    for subject in subjects:
        raw_chunks = _shared_doc_chunks(subject) + _notes_chunks(subject) + _transcript_chunks(subject)
        print(f"[search_index] {subject}: {len(raw_chunks)} candidate chunks")

        for i, chunk in enumerate(raw_chunks):
            key = (chunk["subject"], chunk["source_type"], chunk["label"])
            if "embedding" not in chunk:
                cached = existing_by_key.get(key)
                if cached and cached.get("text") == chunk["text"]:
                    chunk["embedding"] = cached["embedding"]
                else:
                    chunk["embedding"] = ollama.embed(chunk["text"][:3000])
            all_entries.append(chunk)
            if (i + 1) % 200 == 0:
                print(f"[search_index]   {i + 1}/{len(raw_chunks)} embedded", flush=True)

    write_json(INDEX_PATH, all_entries)
    print(f"[search_index] wrote {len(all_entries)} total entries to {INDEX_PATH}")
    return all_entries
