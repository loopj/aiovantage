"""Relay blind object."""

from dataclasses import dataclass

from aiovantage.object_interfaces import BlindInterface

from .location_object import LocationObject


@dataclass
class RelayBlind(LocationObject, BlindInterface):
    """Relay blind object."""
