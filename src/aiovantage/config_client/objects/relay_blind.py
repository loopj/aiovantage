"""Relay blind object."""

from dataclasses import dataclass

from .blind import Blind


@dataclass
class RelayBlind(Blind):
    """Relay blind object."""
