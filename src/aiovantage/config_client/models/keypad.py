"""Keypad Station."""

from dataclasses import dataclass

from .child_object import ChildObject
from .station_object import StationObject


@dataclass
class Keypad(ChildObject, StationObject):
    """Keypad Station."""
