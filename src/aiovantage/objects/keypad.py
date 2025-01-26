"""Keypad Station."""

from dataclasses import dataclass

from .station_object import StationObject
from .types import Parent


@dataclass(kw_only=True)
class Keypad(StationObject):
    """Keypad Station."""

    parent: Parent
