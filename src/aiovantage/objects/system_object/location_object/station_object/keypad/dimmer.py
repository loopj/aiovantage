"""ScenePoint Dimmer Station."""

from dataclasses import dataclass

from . import Keypad


@dataclass
class Dimmer(Keypad):
    """ScenePoint Dimmer Station."""
