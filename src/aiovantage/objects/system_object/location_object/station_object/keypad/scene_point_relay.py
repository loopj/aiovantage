"""ScenePoint Relay Station."""

from dataclasses import dataclass

from . import Keypad


@dataclass(kw_only=True)
class ScenePointRelay(Keypad):
    """ScenePoint Relay Station."""
