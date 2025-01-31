"""Keypad Station."""

from dataclasses import dataclass

from aiovantage.object_interfaces import SounderInterface

from .station_object import StationObject
from .types import Parent


@dataclass(kw_only=True)
class Keypad(StationObject, SounderInterface):
    """Keypad Station."""

    parent: Parent
