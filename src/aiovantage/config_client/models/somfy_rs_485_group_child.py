"""Somfy RS-485 SDN 2.0 blind group."""

from dataclasses import dataclass

from .blind_group_base import BlindGroupBase
from .child_device import ChildDevice


@dataclass
class SomfyRS485GroupChild(BlindGroupBase, ChildDevice):
    """Somfy RS-485 SDN 2.0 blind group."""

    class Meta:
        name = "Somfy.RS-485_Group_CHILD"
