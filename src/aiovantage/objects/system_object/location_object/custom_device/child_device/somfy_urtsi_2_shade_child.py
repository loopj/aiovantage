"""Somfy URTSI 2 blind."""

from dataclasses import dataclass

from aiovantage.object_interfaces.blind import BlindInterface

from . import ChildDevice


@dataclass(kw_only=True)
class SomfyURTSI2ShadeChild(ChildDevice, BlindInterface):
    """Somfy URTSI 2 blind."""

    class Meta:
        name = "Somfy.URTSI_2_Shade_CHILD"
