"""Relay blind object."""

from dataclasses import dataclass

from .blind_base import BlindBase
from .location_object import LocationObject


@dataclass
class RelayBlind(BlindBase, LocationObject):
    """Relay blind object."""
