from __future__ import annotations

from dressmaker_trainer.drivers.base import BaseDriver
from dressmaker_trainer.drivers.input_driver import InputDriver
from dressmaker_trainer.drivers.overlay_driver import OverlayDriver
from dressmaker_trainer.drivers.log_driver import LogDriver

_DRIVERS: dict[str, type[BaseDriver]] = {
    "input": InputDriver,
    "overlay": OverlayDriver,
    "log": LogDriver,
}


def build_driver(name: str, params: dict[str, object] | None = None) -> BaseDriver:
    if name not in _DRIVERS:
        raise KeyError(f"driver not registered: {name}")
    return _DRIVERS[name](params)