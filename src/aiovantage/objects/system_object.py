"""Base class for all objects."""

import datetime as dt
from dataclasses import dataclass, field

from aiovantage.object_interfaces import ObjectInterface
from aiovantage.object_interfaces.base import Interface


@dataclass(kw_only=True)
class SystemObject(ObjectInterface):
    """Base class for all objects."""

    # MTime, DName, not available in 2.x firmware

    vid: int = field(metadata={"name": "VID", "type": "Attribute"})
    master: int = field(metadata={"type": "Attribute"})
    name: str
    model: str
    note: str
    d_name: str | None = None
    m_time: dt.datetime | None = field(
        default=None,
        metadata={"type": "Attribute", "format": "%Y-%m-%dT%H:%M:%S.%f"},
    )

    @property
    def id(self) -> int:
        """Return the Vantage ID of the object."""
        return self.vid

    @property
    def display_name(self) -> str:
        """Return the display name of the object."""
        return self.d_name or self.name

    @classmethod
    def element_name(cls) -> str:
        """Return the Vantage XML element name for this object."""
        cls_meta = getattr(cls, "Meta", None)
        return getattr(cls_meta, "name", cls.__qualname__)

    @classmethod
    def object_interfaces(cls) -> list[type[Interface]]:
        """Return the interfaces that this object implements."""
        return [
            base
            for base in cls.__mro__
            if Interface in base.__bases__ and base is not Interface
        ]
