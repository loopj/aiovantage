"""Relay blind object."""

from dataclasses import dataclass

from aiovantage.object_interfaces.blind import BlindInterface
from aiovantage.objects.location_object import LocationObject


@dataclass
class RelayBlind(LocationObject, BlindInterface):
    """Relay blind object."""
