"""Screenshot analysis via the local multimodal Ollama model."""

import base64
from pathlib import Path

from .common import Ollama

VISION_PROMPT = """You are looking at a single frame captured from a recorded MBA business-school \
lecture (accounting / management / statistics / marketing). The frame may show a slide, a \
whiteboard, an Excel/PDF walkthrough, or just the speaker's webcam.

Decide first: is there any substantive academic content clearly visible (text, a table, a \
journal entry, a ledger, a formula, a chart, a diagram)?

- If NO (it's just a talking head, a blank/transition slide, or unreadable) reply with exactly: SKIP
- If YES, respond in this format:
  TITLE: <short label for what's on screen>
  If it is primarily a table, journal entry, ledger, or any tabular data: transcribe it \
faithfully as a GitHub-Flavored Markdown table (reconstruct rows/columns exactly; do not \
invent numbers you can't read — write "?" for illegible cells).
  Otherwise (diagram/chart/freeform notes): write a concise but complete description of the \
content, preserving any numbers, labels, or step-by-step structure shown.
"""


def analyze_screenshot(image_path: Path, ollama: Ollama, evict: bool = False, max_tokens: int = 500) -> dict | None:
    b64 = base64.b64encode(image_path.read_bytes()).decode()
    response = ollama.generate(VISION_PROMPT, images=[b64], evict=evict, max_tokens=max_tokens).strip()
    if response.upper().startswith("SKIP"):
        return None
    return {"path": str(image_path), "analysis": response}
