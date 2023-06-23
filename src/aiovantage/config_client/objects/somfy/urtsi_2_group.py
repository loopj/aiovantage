"""Somfy URTSI 2 blind group."""

from dataclasses import dataclass

from aiovantage.config_client.objects.blind_group import BlindGroup


@dataclass
class URTSI2Group(BlindGroup):
    """Somfy URTSI 2 blind group."""

    class Meta:
        """Meta class."""

        name = "Somfy.URTSI_2_Group_CHILD"
