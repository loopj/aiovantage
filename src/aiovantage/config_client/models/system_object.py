"""Base class for all objects."""

from typing import Optional

from attr import define, field
from xsdata.models.datatype import XmlDateTime


@define(kw_only=True, slots=False)
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
            "name": "MTimes",
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
