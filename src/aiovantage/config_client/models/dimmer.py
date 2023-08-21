"""ScenePoint Dimmer Station."""

from attr import define

from .keypad import Keypad


@define
class Dimmer(Keypad):
    """ScenePoint Dimmer Station."""
