#!/usr/bin/env python3
"""Local hybrid search over the whole corpus (shared course docs + generated notes + raw
transcripts, both subjects): BM25 (lexical) and embeddings (semantic) are ranked separately,
then combined via Reciprocal Rank Fusion (RRF) — a doc's final score is 1/(k+rank_bm25) +
1/(k+rank_embed), so it only needs to rank well on ONE signal to surface, but ranking well on
BOTH pushes it to the top. This is the standard, simple way to combine two rankers without
needing to normalize/calibrate their raw scores against each other.

Usage: ../.venv/bin/python3 search_server.py
Then open http://127.0.0.1:5050 in a browser.
"""

from contextlib import asynccontextmanager

import numpy as np
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from rank_bm25 import BM25Okapi

from lib.common import Ollama, REPO_ROOT, load_config, read_json
from lib.search_index import INDEX_PATH

RRF_K = 60
TOP_N = 20


@asynccontextmanager
async def lifespan(_app: FastAPI):
    load_index()
    yield


app = FastAPI(lifespan=lifespan)
CONFIG = load_config()
OLLAMA = Ollama(CONFIG)
INDEX: list[dict] = []


def _tokenize(text: str) -> list[str]:
    return text.lower().split()


def load_index():
    global INDEX
    INDEX = read_json(INDEX_PATH, default=[])
    print(f"[search_server] loaded {len(INDEX)} entries from {INDEX_PATH}")


def _rrf_search(query: str, subjects: list[str] | None) -> list[dict]:
    pool = [e for e in INDEX if not subjects or e["subject"] in subjects]
    if not pool:
        return []

    # --- BM25 (lexical) ranking ---
    tokenized_corpus = [_tokenize(e["text"]) for e in pool]
    bm25 = BM25Okapi(tokenized_corpus)
    bm25_scores = bm25.get_scores(_tokenize(query))
    bm25_order = np.argsort(-bm25_scores)
    bm25_rank = {int(idx): rank for rank, idx in enumerate(bm25_order)}

    # --- Embedding (semantic) ranking ---
    q_emb = np.array(OLLAMA.embed(query))
    q_norm = np.linalg.norm(q_emb) or 1.0
    doc_embs = np.array([e["embedding"] for e in pool])
    doc_norms = np.linalg.norm(doc_embs, axis=1)
    doc_norms[doc_norms == 0] = 1.0
    cos_sims = (doc_embs @ q_emb) / (doc_norms * q_norm)
    embed_order = np.argsort(-cos_sims)
    embed_rank = {int(idx): rank for rank, idx in enumerate(embed_order)}

    # --- Reciprocal Rank Fusion ---
    scored = []
    for i in range(len(pool)):
        rrf_score = 1 / (RRF_K + bm25_rank[i] + 1) + 1 / (RRF_K + embed_rank[i] + 1)
        scored.append((rrf_score, i))
    scored.sort(key=lambda x: -x[0])

    results = []
    for rrf_score, i in scored[:TOP_N]:
        e = pool[i]
        results.append({
            "subject": e["subject"],
            "source_type": e["source_type"],
            "label": e["label"],
            "snippet": e["text"][:400],
            "link": e["link"],
            "rrf_score": round(rrf_score, 4),
            "bm25_rank": bm25_rank[i] + 1,
            "embed_rank": embed_rank[i] + 1,
        })
    return results


@app.get("/api/search")
def api_search(q: str = "", subjects: str = ""):
    query = q.strip()
    subject_list = [s for s in subjects.split(",") if s] or None
    if not query:
        return JSONResponse({"results": []})
    return JSONResponse({"results": _rrf_search(query, subject_list)})


@app.get("/api/subjects")
def api_subjects():
    return JSONResponse({"subjects": CONFIG["subjects"]})


@app.get("/", response_class=HTMLResponse)
def index_page():
    return PAGE_HTML


PAGE_HTML = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Lecture Search</title>
<style>
  :root { color-scheme: light dark; }
  body { font-family: -apple-system, Segoe UI, sans-serif; max-width: 800px; margin: 0 auto; padding: 24px; }
  h1 { font-size: 20px; }
  #searchbar { display: flex; gap: 8px; margin-bottom: 12px; }
  #q { flex: 1; padding: 10px 12px; font-size: 15px; border-radius: 6px; border: 1px solid #999; }
  #subjects { display: flex; gap: 12px; margin-bottom: 16px; font-size: 13px; flex-wrap: wrap; }
  .result { border: 1px solid #ccc; border-radius: 8px; padding: 12px 14px; margin-bottom: 10px; }
  .meta { font-size: 12px; opacity: 0.7; margin-bottom: 4px; }
  .badge { display: inline-block; padding: 1px 6px; border-radius: 4px; font-size: 11px; margin-right: 6px; background: #eee; color: #333; }
  .snippet { font-size: 14px; line-height: 1.4; }
  .ranks { font-size: 11px; opacity: 0.6; margin-top: 4px; }
  #status { font-size: 13px; opacity: 0.6; margin-bottom: 10px; }
</style>
</head>
<body>
<h1>Lecture Search</h1>
<div id="subjects"></div>
<div id="searchbar">
  <input id="q" type="text" placeholder="Search across transcripts, notes, and course materials..." autofocus>
</div>
<div id="status"></div>
<div id="results"></div>

<script>
let allSubjects = [];
let selectedSubjects = new Set();

async function loadSubjects() {
  const res = await fetch('/api/subjects');
  const data = await res.json();
  allSubjects = data.subjects;
  selectedSubjects = new Set(allSubjects);
  renderSubjectFilters();
}

function renderSubjectFilters() {
  const el = document.getElementById('subjects');
  el.innerHTML = allSubjects.map(s => `
    <label><input type="checkbox" value="${s}" ${selectedSubjects.has(s) ? 'checked' : ''}> ${s}</label>
  `).join('');
  el.querySelectorAll('input').forEach(cb => {
    cb.addEventListener('change', () => {
      if (cb.checked) selectedSubjects.add(cb.value); else selectedSubjects.delete(cb.value);
      runSearch();
    });
  });
}

let debounceTimer;
document.getElementById('q').addEventListener('input', () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(runSearch, 350);
});

async function runSearch() {
  const q = document.getElementById('q').value.trim();
  const statusEl = document.getElementById('status');
  const resultsEl = document.getElementById('results');
  if (!q) { resultsEl.innerHTML = ''; statusEl.textContent = ''; return; }
  statusEl.textContent = 'Searching...';
  const subjParam = Array.from(selectedSubjects).join(',');
  const res = await fetch(`/api/search?q=${encodeURIComponent(q)}&subjects=${encodeURIComponent(subjParam)}`);
  const data = await res.json();
  statusEl.textContent = `${data.results.length} result(s)`;
  resultsEl.innerHTML = data.results.map(r => `
    <div class="result">
      <div class="meta"><span class="badge">${r.subject}</span><span class="badge">${r.source_type}</span>${r.label}</div>
      <div class="snippet">${r.snippet.replace(/</g, '&lt;')}</div>
      <div class="ranks">RRF ${r.rrf_score} &middot; BM25 rank #${r.bm25_rank} &middot; embedding rank #${r.embed_rank} &middot; ${r.link}</div>
    </div>
  `).join('');
}

loadSubjects();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    load_index()
    print(f"Serving at http://127.0.0.1:5050 (repo root: {REPO_ROOT})")
    uvicorn.run(app, host="127.0.0.1", port=5050)
