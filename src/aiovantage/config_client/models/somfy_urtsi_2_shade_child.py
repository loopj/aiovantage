"""Somfy URTSI 2 blind."""

from attr import define

from .blind_base import BlindBase
from .child_device import ChildDevice


@define
class SomfyURTSI2ShadeChild(BlindBase, ChildDevice):
    """Somfy URTSI 2 blind."""

    class Meta:
        name = "Somfy.URTSI_2_Shade_CHILD"
