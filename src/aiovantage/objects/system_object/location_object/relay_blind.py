"""Relay blind object."""

from dataclasses import dataclass

from aiovantage.object_interfaces.blind import BlindInterface

from . import LocationObject


@dataclass(kw_only=True)
class RelayBlind(LocationObject, BlindInterface):
    """Relay blind object."""
