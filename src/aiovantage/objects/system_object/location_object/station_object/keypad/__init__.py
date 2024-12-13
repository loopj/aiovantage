"""Keypad Station."""

from dataclasses import dataclass

from aiovantage.object_interfaces import SounderInterface
from aiovantage.objects.types import Parent

from .. import StationObject


@dataclass(kw_only=True)
class Keypad(StationObject, SounderInterface):
    """Keypad Station."""

    parent: Parent
