"""DryContact object."""

from dataclasses import dataclass

from .child_object import ChildObject
from .location_object import LocationObject


@dataclass
class DryContact(LocationObject, ChildObject):
    """DryContact object."""

    def __post_init__(self) -> None:
        """Declare state attributes in post init."""
        self.triggered: bool = False
