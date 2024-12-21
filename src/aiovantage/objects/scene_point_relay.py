"""ScenePoint Relay Station."""

from dataclasses import dataclass

from .keypad import Keypad


@dataclass(kw_only=True)
class ScenePointRelay(Keypad):
    """ScenePoint Relay Station."""
