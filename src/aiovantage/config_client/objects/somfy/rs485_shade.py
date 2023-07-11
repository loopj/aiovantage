"""Somfy RS-485 SDN 2.0 blind."""
# pylint: disable=relative-beyond-top-level

from dataclasses import dataclass

from ..blind_base import BlindBase
from ..child_device import ChildDevice


@dataclass
class RS485Shade(BlindBase, ChildDevice):
    """Somfy RS-485 SDN 2.0 blind."""

    class Meta:
        """Meta class."""

        name = "Somfy.RS-485_Shade_CHILD"
