"""Base class for all objects."""

from dataclasses import dataclass, field

from xsdata.models.datatype import XmlDateTime


@dataclass
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

    mtime: XmlDateTime = field(
        metadata={
            "name": "MTime",
            "type": "Attribute",
        }
    )

    name: str = field(
        metadata={
            "name": "Name",
        }
    )

    note: str = field(
        metadata={
            "name": "Note",
        }
    )

    model: str = field(
        metadata={
            "name": "Model",
        }
    )

    display_name: str = field(
        metadata={
            "name": "DName",
        }
    )
