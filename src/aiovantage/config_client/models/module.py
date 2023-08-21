"""Module object."""

from attr import define, field

from .system_object import SystemObject
from .types import Parent


@define
class Module(SystemObject):
    """Module object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )
