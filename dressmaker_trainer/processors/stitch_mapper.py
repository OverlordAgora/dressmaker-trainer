"""Maps detected anchors into stitch-plan coordinates."""
from __future__ import annotations

import math

from dressmaker_trainer.processors.base import BaseProcessor, Frame
from dressmaker_trainer.processors.registry import register_processor


@register_processor("stitch_mapper")
class StitchMapper(BaseProcessor):
    def __init__(self, params: dict[str, object] | None = None) -> None:
        super().__init__(params)
        self.grid = float(self.params.get("grid", 24.0))
        self.max_targets = int(self.params.get("max_targets", 6))

    def process(self, frame: Frame) -> Frame | None:
        anchors = frame.meta.get("anchors") or []
        targets = []
        for a in anchors[: self.max_targets]:
            x, y, w, h = a["bbox"]  # type: ignore[index]
            cx = int(x + w / 2)
            cy = int(y + h / 2)
            gx = int(math.floor(cx / self.grid))
            gy = int(math.floor(cy / self.grid))
            targets.append({"screen": (cx, cy), "grid": (gx, gy)})
        frame.meta["targets"] = targets
        return frame