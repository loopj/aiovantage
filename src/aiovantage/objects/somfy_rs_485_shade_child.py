"""Somfy RS-485 SDN 2.0 blind."""

from dataclasses import dataclass

from .blind_base import BlindBase
from .child_device import ChildDevice


@dataclass(kw_only=True)
class SomfyRS485ShadeChild(BlindBase, ChildDevice):
    """Somfy RS-485 SDN 2.0 blind."""

    class Meta:
        name = "Somfy.RS-485_Shade_CHILD"
