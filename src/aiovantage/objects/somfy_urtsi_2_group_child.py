"""Somfy URTSI 2 blind group."""

from dataclasses import dataclass

from aiovantage.object_interfaces.blind import BlindInterface
from aiovantage.objects.child_device import ChildDevice


@dataclass
class SomfyURTSI2GroupChild(ChildDevice, BlindInterface):
    """Somfy URTSI 2 blind group."""

    class Meta:
        name = "Somfy.URTSI_2_Group_CHILD"
