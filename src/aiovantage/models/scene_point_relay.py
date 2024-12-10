"""ScenePoint Relay Station."""

from dataclasses import dataclass

from aiovantage.models.keypad import Keypad


@dataclass
class ScenePointRelay(Keypad):
    """ScenePoint Relay Station."""
