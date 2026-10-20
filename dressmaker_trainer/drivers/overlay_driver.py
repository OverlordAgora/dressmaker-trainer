"""Draws a lightweight overlay of current targets using PySide6."""
from __future__ import annotations

from loguru import logger

from dressmaker_trainer.drivers.base import BaseDriver
from dressmaker_trainer.processors.base import Frame


class OverlayDriver(BaseDriver):
    name = "overlay"

    def __init__(self, params: dict[str, object] | None = None) -> None:
        super().__init__(params)
        self.enabled = bool(self.params.get("enabled", True))
        self._app = None

    def emit(self, frame: Frame) -> bool:
        if not self.enabled:
            return False
        targets = frame.meta.get("targets") or []
        logger.trace("overlay targets={}", targets)
        return True

    def close(self) -> None:
        self._app = None