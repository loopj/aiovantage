"""Somfy URTSI 2 blind."""
# pylint: disable=relative-beyond-top-level

from dataclasses import dataclass

from ..blind_base import BlindBase
from ..child_device import ChildDevice


@dataclass
class URTSI2Shade(BlindBase, ChildDevice):
    """Somfy URTSI 2 blind."""

    class Meta:
        """Meta class."""

        name = "Somfy.URTSI_2_Shade_CHILD"
