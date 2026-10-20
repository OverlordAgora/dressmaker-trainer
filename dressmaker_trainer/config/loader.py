"""Load and validate trainer profiles from TOML."""
from __future__ import annotations

from pathlib import Path
from typing import Literal

import tomli
from pydantic import BaseModel, Field


class CaptureConfig(BaseModel):
    backend: Literal["dxgi", "gdi", "win32"] = "dxgi"
    region: tuple[int, int, int, int] = Field(default=(0, 0, 1920, 1080))
    fps_cap: int = 60


class ProcessorConfig(BaseModel):
    name: str
    enabled: bool = True
    params: dict[str, float | int | str] = Field(default_factory=dict)


class DriverConfig(BaseModel):
    name: Literal["input", "overlay", "log"] = "log"
    enabled: bool = True
    params: dict[str, float | int | str] = Field(default_factory=dict)


class TrainerConfig(BaseModel):
    profile: str = "default"
    capture: CaptureConfig = Field(default_factory=CaptureConfig)
    processors: list[ProcessorConfig] = Field(default_factory=list)
    drivers: list[DriverConfig] = Field(default_factory=list)


def load_config(path: Path, profile: str = "default") -> TrainerConfig:
    if not path.exists():
        raise FileNotFoundError(f"config not found: {path}")
    raw = tomli.loads(path.read_text(encoding="utf-8"))
    section = raw.get("profiles", {}).get(profile, raw)
    section.setdefault("profile", profile)
    return TrainerConfig.model_validate(section)