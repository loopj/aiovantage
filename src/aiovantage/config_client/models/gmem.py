"""GMem (variable) object."""

from typing import Union

from attr import define, field

from .system_object import SystemObject


@define
class Tag:
    """GMem tag."""

    type: str

    object: bool = field(
        default=False,
        metadata={
            "name": "object",
            "type": "Attribute",
        },
    )


@define
class Data:
    """GMem data."""

    fixed: bool = field(
        default=False,
        metadata={
            "name": "Fixed",
            "type": "Attribute",
        },
    )


@define
class GMem(SystemObject):
    """GMem (variable) object."""

    data: Data = field(
        metadata={
            "name": "data",
        }
    )

    persistent: bool = field(
        metadata={
            "name": "Persistent",
        }
    )

    tag: Tag = field(
        metadata={
            "name": "Tag",
        }
    )

    value: Union[int, str, bool, None] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

    @property
    def is_bool(self) -> bool:
        """Return True if GMem is boolean type."""
        return self.tag.type == "bool"

    @property
    def is_str(self) -> bool:
        """Return True if GMem is string type."""
        return self.tag.type == "Text"

    @property
    def is_int(self) -> bool:
        """Return True if GMem is integer type."""
        return self.tag.type in (
            "Delay",
            "DeviceUnits",
            "Level",
            "Load",
            "Number",
            "Seconds",
            "Task",
            "DegC",
        )

    @property
    def is_object_id(self) -> bool:
        """Return True if GMem is a pointer to an object."""
        return self.tag.object

    @property
    def is_fixed(self) -> bool:
        """Return True if GMem is a fixed point number."""
        return self.data.fixed
