"""Base class for all objects."""

import datetime as dt
from dataclasses import dataclass, field

from aiovantage.object_interfaces.object import ObjectInterface


@dataclass(kw_only=True)
class SystemObject(ObjectInterface):
    """Base class for all objects."""

    id: int = field(
        metadata={
            "name": "VID",
            "type": "Attribute",
        }
    )

    master_id: int = field(
        metadata={
            "name": "Master",
            "type": "Attribute",
        }
    )

    name: str = field(
        metadata={
            "name": "Name",
        }
    )

    model: str = field(
        metadata={
            "name": "Model",
        }
    )

    note: str = field(
        metadata={
            "name": "Note",
        }
    )

    # Not available in 2.x firmware
    mtime: dt.datetime | None = field(
        default=None,
        metadata={
            "name": "MTime",
            "type": "Attribute",
            "format": "%Y-%m-%dT%H:%M:%S.%f",
        },
    )

    # Not available in 2.x firmware
    display_name: str | None = field(
        default=None,
        metadata={
            "name": "DName",
        },
    )

    @classmethod
    def vantage_type(cls) -> str:
        """Return the Vantage type of the object."""
        cls_meta = getattr(cls, "Meta", None)
        return getattr(cls_meta, "name", cls.__qualname__)
