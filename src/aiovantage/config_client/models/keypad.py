"""Keypad Station."""

from attr import define

from .child_object import ChildObject
from .station_object import StationObject


@define
class Keypad(ChildObject, StationObject):
    """Keypad Station."""
