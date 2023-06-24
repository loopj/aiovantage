"""Somfy RS-485 SDN 2.0 blind group."""

from dataclasses import dataclass

from aiovantage.config_client.objects.blind_group import BlindGroup


@dataclass
class RS485Group(BlindGroup):
    """Somfy RS-485 SDN 2.0 blind group."""

    class Meta:
        """Meta class."""

        name = "Somfy.RS-485_Group_CHILD"
