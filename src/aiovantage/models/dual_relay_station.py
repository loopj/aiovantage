"""ScenePoint Dual Relay Station."""

from dataclasses import dataclass

from aiovantage.models.keypad import Keypad
from aiovantage.object_interfaces import SounderInterface


@dataclass
class DualRelayStation(Keypad, SounderInterface):
    """ScenePoint Dual Relay Station."""
