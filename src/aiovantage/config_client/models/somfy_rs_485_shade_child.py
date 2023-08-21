"""Somfy RS-485 SDN 2.0 blind."""

from attr import define

from .blind_base import BlindBase
from .child_device import ChildDevice


@define
class SomfyRS485ShadeChild(BlindBase, ChildDevice):
    """Somfy RS-485 SDN 2.0 blind."""

    class Meta:
        name = "Somfy.RS-485_Shade_CHILD"
