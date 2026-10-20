"""Centralized loguru configuration."""
from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger


def setup_logging(level: str = "INFO") -> None:
    logger.remove()
    logger.add(sys.stderr, level=level, backtrace=False, diagnose=False)
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logger.add(
        log_dir / "trainer.log",
        level="DEBUG",
        rotation="5 MB",
        retention=3,
        enqueue=True,
    )