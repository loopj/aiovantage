"""ScenePoint Dual Relay Station."""

from dataclasses import dataclass

from aiovantage.object_interfaces import SounderInterface
from aiovantage.objects.keypad import Keypad


@dataclass
class DualRelayStation(Keypad, SounderInterface):
    """ScenePoint Dual Relay Station."""
