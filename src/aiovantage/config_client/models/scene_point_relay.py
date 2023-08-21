"""ScenePoint Relay Station."""

from attr import define

from .keypad import Keypad


@define
class ScenePointRelay(Keypad):
    """ScenePoint Relay Station."""
