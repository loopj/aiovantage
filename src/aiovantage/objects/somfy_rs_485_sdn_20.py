"""Somfy RS-485 SDN 2.0 driver objects."""

from dataclasses import dataclass

from .blind_base import BlindBase
from .blind_group_base import BlindGroupBase
from .child_device import ChildDevice
from .port_device import PortDevice


@dataclass(kw_only=True)
class SomfyRS485SDN20Port(PortDevice):
    """Somfy RS-485 SDN 2.0 port device."""

    class Meta:
        name = "Somfy.RS-485_SDN_2_x2E_0_PORT"


@dataclass(kw_only=True)
class SomfyRS485ShadeChild(BlindBase, ChildDevice):
    """Somfy RS-485 SDN 2.0 blind."""

    class Meta:
        name = "Somfy.RS-485_Shade_CHILD"


@dataclass(kw_only=True)
class SomfyRS485GroupChild(BlindGroupBase, ChildDevice):
    """Somfy RS-485 SDN 2.0 blind group."""

    class Meta:
        name = "Somfy.RS-485_Group_CHILD"
