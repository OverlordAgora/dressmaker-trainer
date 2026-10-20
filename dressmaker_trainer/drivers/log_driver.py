"""Logs each processed frame summary for debugging the pipeline."""
from __future__ import annotations

from loguru import logger

from dressmaker_trainer.drivers.base import BaseDriver
from dressmaker_trainer.processors.base import Frame


class LogDriver(BaseDriver):
    name = "log"

    def __init__(self, params: dict[str, object] | None = None) -> None:
        super().__init__(params)
        self.verbose = bool(self.params.get("verbose", False))
        self._count = 0

    def emit(self, frame: Frame) -> bool:
        self._count += 1
        if self.verbose or self._count % 30 == 0:
            logger.info(
                "frame ts={:.3f} anchors={} targets={}",
                frame.timestamp,
                frame.meta.get("anchor_count", 0),
                len(frame.meta.get("targets") or []),
            )
        return True