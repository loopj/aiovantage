"""Base class for all objects."""

import datetime as dt
from dataclasses import dataclass, field

from aiovantage.object_interfaces import ObjectInterface


@dataclass(kw_only=True)
class SystemObject(ObjectInterface):
    """Base class for all objects."""

    vid: int = field(metadata={"name": "VID", "type": "Attribute"})
    master: int = field(metadata={"type": "Attribute"})
    name: str
    model: str
    note: str

    # Not available in 2.x firmware
    d_name: str = ""
    m_time: dt.datetime | None = field(
        default=None,
        metadata={"type": "Attribute", "format": "%Y-%m-%dT%H:%M:%S.%f"},
    )

    @property
    def id(self) -> int:
        """Return the ID of the object."""
        return self.vid

    @classmethod
    def vantage_type(cls) -> str:
        """Return the Vantage type for this object."""
        cls_meta = getattr(cls, "Meta", None)
        return getattr(cls_meta, "name", cls.__qualname__)
