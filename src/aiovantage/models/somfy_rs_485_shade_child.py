"""Somfy RS-485 SDN 2.0 blind."""

from dataclasses import dataclass

from aiovantage.models.child_device import ChildDevice
from aiovantage.object_interfaces.blind import BlindInterface


@dataclass
class SomfyRS485ShadeChild(ChildDevice, BlindInterface):
    """Somfy RS-485 SDN 2.0 blind."""

    class Meta:
        name = "Somfy.RS-485_Shade_CHILD"
