"""Somfy URTSI 2 blind group."""
# pylint: disable=relative-beyond-top-level

from dataclasses import dataclass

from ..blind_group_base import BlindGroupBase
from ..child_device import ChildDevice


@dataclass
class URTSI2Group(BlindGroupBase, ChildDevice):
    """Somfy URTSI 2 blind group."""

    class Meta:
        """Meta class."""

        name = "Somfy.URTSI_2_Group_CHILD"
