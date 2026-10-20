"""Synthesizes keystrokes / mouse movement toward mapped targets.

Educational use only. Uses Win32 SendInput via pyautogui.
"""
from __future__ import annotations

import time

import pyautogui
from loguru import logger

from dressmaker_trainer.drivers.base import BaseDriver
from dressmaker_trainer.processors.base import Frame

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.0


class InputDriver(BaseDriver):
    name = "input"

    def __init__(self, params: dict[str, object] | None = None) -> None:
        super().__init__(params)
        self.cooldown = float(self.params.get("cooldown_ms", 120)) / 1000.0
        self.smooth = float(self.params.get("smooth", 0.35))
        self._last = 0.0

    def emit(self, frame: Frame) -> bool:
        now = time.monotonic()
        if now - self._last < self.cooldown:
            return False
        targets = frame.meta.get("targets") or []
        if not targets:
            return False
        tx, ty = targets[0]["screen"]  # type: ignore[index]
        try:
            pyautogui.moveTo(tx, ty, duration=self.smooth)
            pyautogui.click()
        except Exception as exc:  # pragma: no cover - desktop dependent
            logger.warning("input emit failed: {}", exc)
            return False
        self._last = now
        return True