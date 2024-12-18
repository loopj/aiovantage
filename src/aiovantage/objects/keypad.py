"""Keypad Station."""

from dataclasses import dataclass

from .station_object import StationObject
from .types import Parent


@dataclass
class Keypad(StationObject):
    """Keypad Station."""

    parent: Parent
