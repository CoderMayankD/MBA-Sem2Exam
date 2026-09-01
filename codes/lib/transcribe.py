"""Audio extraction (ffmpeg) + transcription (faster-whisper), with disk caching."""

import subprocess
import tempfile
from pathlib import Path

import imageio_ffmpeg

from .common import cache_dir, file_hash, read_json, write_json

_whisper_model = None  # loaded once per process, reused across videos in a batch


def _ffmpeg_exe() -> str:
    return imageio_ffmpeg.get_ffmpeg_exe()


def extract_audio(video_path: Path) -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="lecture_audio_")) / "audio.wav"
    cmd = [
        _ffmpeg_exe(), "-y", "-i", str(video_path),
        "-vn", "-ac", "1", "-ar", "16000",
        "-loglevel", "error",
        str(tmp),
    ]
    subprocess.run(cmd, check=True)
    return tmp


def get_whisper_model(model_name: str, compute_type: str):
    global _whisper_model
    if _whisper_model is not None:
        return _whisper_model
    from faster_whisper import WhisperModel

    try:
        _whisper_model = WhisperModel(model_name, device="cuda", compute_type=compute_type)
    except Exception as e:
        print(f"[transcribe] GPU init failed ({e}), falling back to CPU (int8) — will be much slower.")
        _whisper_model = WhisperModel(model_name, device="cpu", compute_type="int8")
    return _whisper_model


def transcribe_video(video_path: Path, subject: str, config: dict, force: bool = False) -> list[dict]:
    """Returns a list of {start, end, text} segments. Cached by content hash of the video."""
    vhash = file_hash(video_path)
    cache_path = cache_dir(subject) / "transcripts" / f"{vhash}.json"

    if not force:
        cached = read_json(cache_path)
        if cached is not None:
            return cached["segments"]

    print(f"[transcribe] {video_path.name}")
    audio_path = extract_audio(video_path)
    try:
        from faster_whisper import BatchedInferencePipeline

        model = get_whisper_model(
            config["models"]["whisper_model"], config["models"]["whisper_compute_type"]
        )
        try:
            pipeline = BatchedInferencePipeline(model=model)
            segments_iter, info = pipeline.transcribe(str(audio_path), batch_size=16)
        except Exception:
            segments_iter, info = model.transcribe(str(audio_path))

        segments = [
            {"start": s.start, "end": s.end, "text": s.text.strip()} for s in segments_iter
        ]
    finally:
        audio_path.unlink(missing_ok=True)
        audio_path.parent.rmdir()

    write_json(cache_path, {"video": str(video_path), "hash": vhash, "segments": segments})
    return segments
