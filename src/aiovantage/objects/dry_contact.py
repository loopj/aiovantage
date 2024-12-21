"""DryContact object."""

from dataclasses import dataclass

from aiovantage.object_interfaces import ButtonInterface

from .location_object import LocationObject
from .types import Parent


@dataclass(kw_only=True)
class DryContact(LocationObject, ButtonInterface):
    """DryContact object."""

    parent: Parent
