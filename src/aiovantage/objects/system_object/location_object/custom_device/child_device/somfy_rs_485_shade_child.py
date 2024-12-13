"""Somfy RS-485 SDN 2.0 blind."""

from dataclasses import dataclass

from aiovantage.object_interfaces.blind import BlindInterface

from . import ChildDevice


@dataclass(kw_only=True)
class SomfyRS485ShadeChild(ChildDevice, BlindInterface):
    """Somfy RS-485 SDN 2.0 blind."""

    class Meta:
        name = "Somfy.RS-485_Shade_CHILD"
