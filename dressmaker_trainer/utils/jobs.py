"""Small job helpers used by the pipeline runner."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Any


@dataclass
class Job:
    name: str
    fn: Callable[[], Any]
    interval_s: float = 0.0
    last_run: float = field(default=0.0)

    def due(self, now: float | None = None) -> bool:
        now = now or time.monotonic()
        return now - self.last_run >= self.interval_s

    def run(self) -> Any:
        self.last_run = time.monotonic()
        return self.fn()