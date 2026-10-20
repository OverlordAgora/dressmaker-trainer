"""Win32 GDI capture backend used when DXGI is unavailable."""
from __future__ import annotations

import time

import numpy as np
import win32gui
import win32ui
from loguru import logger

from dressmaker_trainer.config.loader import CaptureConfig
from dressmaker_trainer.ingest.base import BaseCapture
from dressmaker_trainer.processors.base import Frame


class Win32Capture(BaseCapture):
    def __init__(self, cfg: CaptureConfig) -> None:
        self.region = cfg.region
        self.fps_cap = cfg.fps_cap
        self._hwnd: int = 0

    def start(self) -> None:
        self._hwnd = win32gui.GetDesktopWindow()

    def grab(self) -> Frame | None:
        left, top, width, height = self.region
        try:
            hwnd_dc = win32gui.GetWindowDC(self._hwnd)
            mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
            save_dc = mfc_dc.CreateCompatibleDC()
            bmp = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(mfc_dc, width, height)
            save_dc.SelectObject(bmp)
            save_dc.BitBlt((0, 0), (width, height), mfc_dc, (left, top), 0x00CC0020)
            arr = np.frombuffer(bmp.GetBitmapBits(True), dtype=np.uint8)
            arr = arr.reshape((height, width, 4))[:, :, :3]
            win32gui.DeleteObject(bmp.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(self._hwnd, hwnd_dc)
            return self._to_frame(arr, time.time())
        except Exception as exc:  # pragma: no cover - backend dependent
            logger.debug("win32 grab failed: {}", exc)
            return None

    def stop(self) -> None:
        self._hwnd = 0