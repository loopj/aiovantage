"""ScenePoint Dimmer Station."""

from dataclasses import dataclass

from .keypad import Keypad


@dataclass(kw_only=True)
class Dimmer(Keypad):
    """ScenePoint Dimmer Station."""
