"""ScenePoint Dual Relay Station."""

from attr import define

from .keypad import Keypad


@define
class DualRelayStation(Keypad):
    """ScenePoint Dual Relay Station."""
