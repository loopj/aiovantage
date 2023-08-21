"""Relay blind object."""

from attr import define

from .blind_base import BlindBase
from .location_object import LocationObject


@define
class RelayBlind(BlindBase, LocationObject):
    """Relay blind object."""
