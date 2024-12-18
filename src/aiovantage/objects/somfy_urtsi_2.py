"""Somfy URTSI 2 objects."""

from dataclasses import dataclass

from aiovantage.object_interfaces import BlindInterface

from .child_device import ChildDevice
from .port_device import PortDevice


@dataclass
class SomfyURTSI2Port(PortDevice):
    """Somfy URTSI 2 port device."""

    class Meta:
        name = "Somfy.URTSI_2_PORT"


@dataclass
class SomfyURTSI2GroupChild(ChildDevice, BlindInterface):
    """Somfy URTSI 2 blind group."""

    class Meta:
        name = "Somfy.URTSI_2_Group_CHILD"


@dataclass
class SomfyURTSI2ShadeChild(ChildDevice, BlindInterface):
    """Somfy URTSI 2 blind."""

    class Meta:
        name = "Somfy.URTSI_2_Shade_CHILD"
