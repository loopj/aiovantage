"""DryContact object."""

from dataclasses import dataclass

from aiovantage.object_interfaces import ButtonInterface

from .location_object import LocationObject
from .types import Parent


@dataclass
class DryContact(LocationObject, ButtonInterface):
    """DryContact object."""

    parent: Parent
