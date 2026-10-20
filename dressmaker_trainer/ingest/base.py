"""Capture backend interface."""
from __future__ import annotations

import abc

import numpy as np

from dressmaker_trainer.processors.base import Frame


class BaseCapture(abc.ABC):
    fps_cap: int = 60

    @abc.abstractmethod
    def start(self) -> None: ...

    @abc.abstractmethod
    def grab(self) -> Frame | None: ...

    @abc.abstractmethod
    def stop(self) -> None: ...

    def _to_frame(self, image: np.ndarray, ts: float) -> Frame:
        return Frame(image=image, timestamp=ts, meta={})