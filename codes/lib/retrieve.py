"""Cosine-similarity top-k retrieval over a subject's cached document embeddings."""

import numpy as np


def top_k(query_embedding: list[float], chunks: list[dict], k: int) -> list[dict]:
    if not chunks:
        return []
    q = np.array(query_embedding)
    q_norm = np.linalg.norm(q) or 1.0

    scored = []
    for c in chunks:
        v = np.array(c["embedding"])
        v_norm = np.linalg.norm(v) or 1.0
        sim = float(np.dot(q, v) / (q_norm * v_norm))
        scored.append((sim, c))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:k]]
