"""Processor contract and Frame dataclass."""
from __future__ import annotations

import abc
from dataclasses import dataclass, field

import numpy as np


@dataclass
class Frame:
    image: np.ndarray
    timestamp: float
    meta: dict[str, object] = field(default_factory=dict)


class BaseProcessor(abc.ABC):
    name: str = "base"

    def __init__(self, params: dict[str, object] | None = None) -> None:
        self.params = params or {}

    @abc.abstractmethod
    def process(self, frame: Frame) -> Frame | None: ...