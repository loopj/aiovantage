"""ScenePoint Dual Relay Station."""

from dataclasses import dataclass

from aiovantage.object_interfaces import SounderInterface

from . import Keypad


@dataclass(kw_only=True)
class DualRelayStation(Keypad, SounderInterface):
    """ScenePoint Dual Relay Station."""
