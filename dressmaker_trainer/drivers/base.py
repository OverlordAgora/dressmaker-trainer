"""Output driver contract."""
from __future__ import annotations

import abc

from dressmaker_trainer.processors.base import Frame


class BaseDriver(abc.ABC):
    name: str = "base"

    def __init__(self, params: dict[str, object] | None = None) -> None:
        self.params = params or {}

    @abc.abstractmethod
    def emit(self, frame: Frame) -> bool: ...

    def close(self) -> None:
        return None