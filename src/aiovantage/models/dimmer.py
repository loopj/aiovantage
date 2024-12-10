"""ScenePoint Dimmer Station."""

from dataclasses import dataclass

from aiovantage.models.keypad import Keypad


@dataclass
class Dimmer(Keypad):
    """ScenePoint Dimmer Station."""
