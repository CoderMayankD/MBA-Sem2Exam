"""Shared helpers: config loading, paths, hashing, Ollama HTTP calls."""

import hashlib
import json
from pathlib import Path

import requests
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.yaml"


def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def subject_dir(subject: str) -> Path:
    return REPO_ROOT / subject


def notes_dir(subject: str) -> Path:
    d = subject_dir(subject) / "Notes"
    d.mkdir(parents=True, exist_ok=True)
    return d


def cache_dir(subject: str) -> Path:
    d = notes_dir(subject) / ".cache"
    (d / "transcripts").mkdir(parents=True, exist_ok=True)
    return d


def file_hash(path: Path, sample_bytes: int = 4_000_000) -> str:
    """Hash file size + head/tail samples rather than the whole (often huge) file, for speed."""
    h = hashlib.sha1()
    size = path.stat().st_size
    h.update(str(size).encode())
    with open(path, "rb") as f:
        h.update(f.read(sample_bytes))
        if size > sample_bytes:
            f.seek(max(0, size - sample_bytes))
            h.update(f.read(sample_bytes))
    return h.hexdigest()[:16]


def slugify(text: str) -> str:
    keep = [c.lower() if c.isalnum() else "-" for c in text]
    slug = "".join(keep)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")


class Ollama:
    def __init__(self, config: dict):
        self.host = config["models"]["ollama_host"].rstrip("/")
        self.llm_model = config["models"]["llm_model"]
        self.embed_model = config["models"]["embed_model"]
        self.keep_alive = config["models"]["keep_alive"]
        # Ollama's default context window (~4096) is far smaller than gemma4:12b actually
        # supports (262144) and silently truncates+empties long prompts (confirmed via server
        # log: "truncating input prompt" / responses cut to 0 chars). Must be requested explicitly.
        self.num_ctx = config["models"].get("num_ctx", 32768)

    def generate(self, prompt: str, images: list[str] | None = None, evict: bool = False, max_tokens: int | None = None) -> str:
        """images: list of base64-encoded image strings (no data: prefix)."""
        options = {"num_ctx": self.num_ctx}
        if max_tokens:
            options["num_predict"] = max_tokens
        payload = {
            "model": self.llm_model,
            "prompt": prompt,
            "stream": False,
            "keep_alive": 0 if evict else self.keep_alive,
            "options": options,
        }
        if images:
            payload["images"] = images
        resp = requests.post(f"{self.host}/api/generate", json=payload, timeout=600)
        resp.raise_for_status()
        return resp.json()["response"]

    def embed(self, text: str) -> list[float]:
        resp = requests.post(
            f"{self.host}/api/embeddings",
            json={"model": self.embed_model, "prompt": text, "keep_alive": self.keep_alive},
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["embedding"]


def read_json(path: Path, default=None):
    if not path.exists():
        return default
    with open(path) as f:
        return json.load(f)


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
