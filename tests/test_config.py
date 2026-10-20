from __future__ import annotations

from pathlib import Path

import pytest

from dressmaker_trainer.config.loader import load_config


SAMPLE = """
[profiles.default]
[profiles.default.capture]
backend = "win32"
region = [0, 0, 800, 600]
fps_cap = 30

[[profiles.default.processors]]
name = "pattern_detector"
params = { threshold = 120, min_area = 500 }

[[profiles.default.drivers]]
name = "log"
params = { verbose = true }
"""


def test_load_profile(tmp_path: Path) -> None:
    cfg_path = tmp_path / "trainer_config.toml"
    cfg_path.write_text(SAMPLE, encoding="utf-8")
    cfg = load_config(cfg_path, profile="default")
    assert cfg.capture.backend == "win32"
    assert cfg.capture.fps_cap == 30
    assert cfg.processors[0].name == "pattern_detector"
    assert cfg.drivers[0].name == "log"


def test_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "nope.toml")