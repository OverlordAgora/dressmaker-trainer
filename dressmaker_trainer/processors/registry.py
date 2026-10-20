from __future__ import annotations

from typing import Callable, Type

from dressmaker_trainer.processors.base import BaseProcessor


_REGISTRY: dict[str, Type[BaseProcessor]] = {}


def register_processor(name: str) -> Callable[[Type[BaseProcessor]], Type[BaseProcessor]]:
    def deco(cls: Type[BaseProcessor]) -> Type[BaseProcessor]:
        cls.name = name
        _REGISTRY[name] = cls
        return cls
    return deco


def build_processor(name: str, params: dict[str, object] | None = None) -> BaseProcessor:
    if name not in _REGISTRY:
        raise KeyError(f"processor not registered: {name}")
    return _REGISTRY[name](params)


def available() -> list[str]:
    return sorted(_REGISTRY)