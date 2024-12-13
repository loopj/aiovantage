"""Somfy RS-485 SDN 2.0 blind group."""

from dataclasses import dataclass

from aiovantage.object_interfaces.blind import BlindInterface
from aiovantage.objects.child_device import ChildDevice


@dataclass
class SomfyRS485GroupChild(ChildDevice, BlindInterface):
    """Somfy RS-485 SDN 2.0 blind group."""

    class Meta:
        name = "Somfy.RS-485_Group_CHILD"
