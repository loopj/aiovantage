"""Somfy RS-485 SDN 2.0 blind group."""
# pylint: disable=relative-beyond-top-level

from dataclasses import dataclass

from ..blind_group_base import BlindGroupBase
from ..child_device import ChildDevice


@dataclass
class RS485Group(BlindGroupBase, ChildDevice):
    """Somfy RS-485 SDN 2.0 blind group."""

    class Meta:
        """Meta class."""

        name = "Somfy.RS-485_Group_CHILD"
