"""Somfy RS-485 SDN 2.0 blind group."""

from attr import define

from .blind_group_base import BlindGroupBase
from .child_device import ChildDevice


@define
class SomfyRS485GroupChild(BlindGroupBase, ChildDevice):
    """Somfy RS-485 SDN 2.0 blind group."""

    class Meta:
        name = "Somfy.RS-485_Group_CHILD"
