"""DryContact object."""

from dataclasses import dataclass

from aiovantage.object_interfaces.button import ButtonInterface
from aiovantage.objects.types import Parent

from . import LocationObject


@dataclass(kw_only=True)
class DryContact(LocationObject, ButtonInterface):
    """DryContact object."""

    parent: Parent
