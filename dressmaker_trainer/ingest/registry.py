from __future__ import annotations

from dressmaker_trainer.config.loader import CaptureConfig
from dressmaker_trainer.ingest.base import BaseCapture
from dressmaker_trainer.ingest.win32_capture import Win32Capture


_CAPTURES = {
    "win32": Win32Capture,
    "gdi": Win32Capture,
    "dxgi": Win32Capture,
}


def build_capture(name: str, cfg: CaptureConfig) -> BaseCapture:
    try:
        cls = _CAPTURES[name]
    except KeyError as exc:
        raise ValueError(f"unknown capture backend: {name}") from exc
    return cls(cfg)