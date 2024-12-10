"""Somfy URTSI 2 blind."""

from dataclasses import dataclass

from aiovantage.models.child_device import ChildDevice
from aiovantage.object_interfaces.blind import BlindInterface


@dataclass
class SomfyURTSI2ShadeChild(ChildDevice, BlindInterface):
    """Somfy URTSI 2 blind."""

    class Meta:
        name = "Somfy.URTSI_2_Shade_CHILD"
