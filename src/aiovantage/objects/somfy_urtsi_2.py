"""Somfy URTSI 2 driver objects."""

from dataclasses import dataclass

from .blind_base import BlindBase
from .blind_group_base import BlindGroupBase
from .child_device import ChildDevice
from .port_device import PortDevice


@dataclass(kw_only=True)
class SomfyURTSI2Port(PortDevice):
    """Somfy URTSI 2 port device."""

    class Meta:
        name = "Somfy.URTSI_2_PORT"


@dataclass(kw_only=True)
class SomfyURTSI2ShadeChild(BlindBase, ChildDevice):
    """Somfy URTSI 2 blind."""

    class Meta:
        name = "Somfy.URTSI_2_Shade_CHILD"


@dataclass(kw_only=True)
class SomfyURTSI2GroupChild(BlindGroupBase, ChildDevice):
    """Somfy URTSI 2 blind group."""

    class Meta:
        name = "Somfy.URTSI_2_Group_CHILD"
