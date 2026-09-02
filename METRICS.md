# Pipeline Metrics

_Snapshot as of 2026-09-02 — Managing People and Organization Lecture 24 (the last recording) is still processing, so lecture-minutes/count will tick up slightly on the next refresh. Everything else is measured directly from the Ollama server log and each note's frontmatter, not estimated._

| Metric | Value |
|---|---|
| Lectures processed | 39 / 40 |
| Lecture-minutes processed | 3,559 min ≈ **59.3 hours** of lecture content |
| Input tokens (prompts sent) | ~2.40 million |
| Output tokens (generated) | ~2.13 million |
| Total LLM requests | ~1,985+ (embeddings + vision + notes; includes this session's testing/debugging, not just final production calls) |
| GPU-active compute time | ~9.2 hrs measured (LLM, from Ollama's own per-request timing logs) + ~3.5 hrs estimated (Whisper transcription, not directly logged) ≈ **~12.7 hours** |
| Electricity consumed (GPU only) | ~12.7 hrs × ~260W sustained draw (measured live at 270W / 97% load; card TDP is 285W) ≈ **~3.3 kWh** |
| Compression ratio | Average lecture ≈ 91 min; each generated note takes ~10-20 min to read ≈ **~6:1** — reading a note takes about a sixth of the time of watching the original lecture |

## Notes on precision

- Token/request counts include exploratory and debugging calls made while building the pipeline this session — real per-lecture cost going forward is lower than the session average implies.
- Whisper's GPU time isn't logged the way Ollama's per-request timing is, so that figure is a reasoned estimate (based on observed transcription speed vs. audio length), not a direct measurement.
- Electricity figure covers GPU power draw only — not the rest of the system (CPU, RAM, disk).
