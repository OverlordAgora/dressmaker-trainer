"""Pipeline runner: wires ingest -> processors -> drivers."""
from __future__ import annotations

import queue
import threading
import time
from typing import Iterable

from loguru import logger

from dressmaker_trainer.config.loader import TrainerConfig
from dressmaker_trainer.ingest.base import BaseCapture
from dressmaker_trainer.ingest.registry import build_capture
from dressmaker_trainer.processors.base import BaseProcessor, Frame
from dressmaker_trainer.processors.registry import build_processor
from dressmaker_trainer.drivers.registry import build_driver
from dressmaker_trainer.drivers.base import BaseDriver


class PipelineRunner:
    def __init__(
        self,
        capture: BaseCapture,
        processors: Iterable[BaseProcessor],
        drivers: Iterable[BaseDriver],
        dry_run: bool = False,
    ) -> None:
        self.capture = capture
        self.processors = list(processors)
        self.drivers = list(drivers)
        self.dry_run = dry_run
        self._queue: queue.Queue[Frame] = queue.Queue(maxsize=8)
        self._stop = threading.Event()

    @classmethod
    def from_config(cls, cfg: TrainerConfig, dry_run: bool = False) -> "PipelineRunner":
        cap = build_capture(cfg.capture.backend, cfg.capture)
        procs = [build_processor(p.name, p.params) for p in cfg.processors if p.enabled]
        drvs = [build_driver(d.name, d.params) for d in cfg.drivers if d.enabled]
        return cls(cap, procs, drvs, dry_run=dry_run)

    def _ingest_loop(self) -> None:
        interval = 1.0 / max(1, self.capture.fps_cap)
        while not self._stop.is_set():
            frame = self.capture.grab()
            if frame is not None:
                try:
                    self._queue.put(frame, timeout=interval)
                except queue.Full:
                    logger.warning("ingest queue full, dropping frame")
            time.sleep(interval)

    def _process_loop(self) -> None:
        while not self._stop.is_set():
            try:
                frame = self._queue.get(timeout=0.25)
            except queue.Empty:
                continue
            for proc in self.processors:
                frame = proc.process(frame)
                if frame is None:
                    break
            if frame is None:
                continue
            for drv in self.drivers:
                if self.dry_run and drv.name == "input":
                    continue
                drv.emit(frame)

    def run_forever(self) -> None:
        self.capture.start()
        threads = [
            threading.Thread(target=self._ingest_loop, name="ingest", daemon=True),
            threading.Thread(target=self._process_loop, name="processor", daemon=True),
        ]
        for t in threads:
            t.start()
        logger.info("pipeline running with {} processors, {} drivers",
                    len(self.processors), len(self.drivers))
        for t in threads:
            t.join()

    def stop(self) -> None:
        self._stop.set()
        self.capture.stop()