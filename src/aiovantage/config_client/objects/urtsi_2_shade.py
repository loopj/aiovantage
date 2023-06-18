"""Somfy URTSI 2 blind."""

from dataclasses import dataclass

from .blind import Blind


@dataclass
class URTSI2Shade(Blind):  # pylint: disable=invalid-name
    """Somfy URTSI 2 blind."""

    class Meta:
        """Meta class."""

        name = "Somfy.URTSI_2_Shade_CHILD"
