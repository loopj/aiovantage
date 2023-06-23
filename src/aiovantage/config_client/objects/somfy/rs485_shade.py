"""Somfy RS-485 SDN 2.0 blind."""

from dataclasses import dataclass

from aiovantage.config_client.objects.blind import Blind


@dataclass
class RS485Shade(Blind):
    """Somfy RS-485 SDN 2.0 blind."""

    class Meta:
        """Meta class."""

        name = "Somfy.RS-485_Shade_CHILD"
