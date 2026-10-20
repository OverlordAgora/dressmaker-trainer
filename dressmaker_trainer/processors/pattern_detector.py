"""Detects dress-pattern anchors in the captured frame."""
from __future__ import annotations

import cv2
import numpy as np

from dressmaker_trainer.processors.base import BaseProcessor, Frame
from dressmaker_trainer.processors.registry import register_processor


@register_processor("pattern_detector")
class PatternDetector(BaseProcessor):
    def __init__(self, params: dict[str, object] | None = None) -> None:
        super().__init__(params)
        self.threshold = int(self.params.get("threshold", 140))
        self.min_area = int(self.params.get("min_area", 900))

    def process(self, frame: Frame) -> Frame | None:
        gray = cv2.cvtColor(frame.image, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, self.threshold, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        anchors = []
        for c in contours:
            if cv2.contourArea(c) < self.min_area:
                continue
            x, y, w, h = cv2.boundingRect(c)
            anchors.append({"bbox": (x, y, w, h), "area": float(cv2.contourArea(c))})
        frame.meta["anchors"] = anchors
        frame.meta["anchor_count"] = len(anchors)
        return frame