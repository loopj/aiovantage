"""Somfy URTSI 2 blind group."""

from attr import define

from .blind_group_base import BlindGroupBase
from .child_device import ChildDevice


@define
class SomfyURTSI2GroupChild(BlindGroupBase, ChildDevice):
    """Somfy URTSI 2 blind group."""

    class Meta:
        name = "Somfy.URTSI_2_Group_CHILD"
