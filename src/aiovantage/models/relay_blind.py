"""Relay blind object."""

from dataclasses import dataclass

from aiovantage.models.location_object import LocationObject
from aiovantage.object_interfaces.blind import BlindInterface


@dataclass
class RelayBlind(LocationObject, BlindInterface):
    """Relay blind object."""
