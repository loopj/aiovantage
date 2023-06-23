"""Somfy URTSI 2 blind."""

from dataclasses import dataclass

from aiovantage.config_client.objects.blind import Blind


@dataclass
class URTSI2Shade(Blind):
    """Somfy URTSI 2 blind."""

    class Meta:
        """Meta class."""

        name = "Somfy.URTSI_2_Shade_CHILD"
