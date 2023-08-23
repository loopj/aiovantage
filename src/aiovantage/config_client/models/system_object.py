"""Base class for all objects."""

from dataclasses import dataclass, field
from typing import Optional

from xsdata.models.datatype import XmlDateTime


@dataclass(kw_only=True)
class SystemObject:
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
    mtime: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "MTime",
            "type": "Attribute",
        },
    )

    # Not available in 2.x firmware
    display_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "DName",
        },
    )
