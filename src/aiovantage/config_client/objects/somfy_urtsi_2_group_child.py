"""Somfy URTSI 2 blind group."""

from dataclasses import dataclass

from .blind_group_base import BlindGroupBase
from .child_device import ChildDevice


@dataclass
class SomfyURTSI2GroupChild(BlindGroupBase, ChildDevice):
    """Somfy URTSI 2 blind group."""

    class Meta:
        name = "Somfy.URTSI_2_Group_CHILD"
