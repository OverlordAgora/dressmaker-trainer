from __future__ import annotations

import numpy as np
import pytest

from dressmaker_trainer.pipeline.runner import PipelineRunner
from dressmaker_trainer.processors.base import BaseProcessor, Frame
from dressmaker_trainer.processors.registry import build_processor, available
from dressmaker_trainer.drivers.base import BaseDriver


class FakeCapture:
    fps_cap = 60

    def __init__(self) -> None:
        self.started = False

    def start(self) -> None:
        self.started = True

    def grab(self) -> Frame | None:
        img = np.zeros((64, 64, 3), dtype=np.uint8)
        return Frame(image=img, timestamp=0.0)

    def stop(self) -> None:
        self.started = False


class CountingDriver(BaseDriver):
    name = "counting"

    def __init__(self) -> None:
        super().__init__({})
        self.count = 0

    def emit(self, frame: Frame) -> bool:
        self.count += 1
        return True


def test_registry_has_core_processors() -> None:
    names = available()
    assert "pattern_detector" in names
    assert "stitch_mapper" in names


def test_pipeline_runs_one_frame() -> None:
    cap = FakeCapture()
    cap.start()
    frame = cap.grab()
    assert frame is not None

    detector = build_processor("pattern_detector", {"threshold": 100, "min_area": 10})
    mapper = build_processor("stitch_mapper", {"grid": 8})
    out = detector.process(frame)
    assert out is not None
    out = mapper.process(out)
    assert out is not None

    drv = CountingDriver()
    assert drv.emit(out) is True
    assert drv.count == 1
    cap.stop()
    assert cap.started is False


@pytest.mark.parametrize("name", ["input", "overlay", "log"])
def test_driver_registry(name: str) -> None:
    from dressmaker_trainer.drivers.registry import build_driver
    drv = build_driver(name, {})
    assert drv.name == name