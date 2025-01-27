"""Base class for DIN station objects."""

from dataclasses import dataclass, field

from .station_object import StationObject


@dataclass(kw_only=True)
class DINStation(StationObject):
    """Base class for DIN station objects."""

    @dataclass
    class DINEnclosure:
        enclosure: int
        position: int = field(metadata={"type": "Attribute"})
        row: int = field(metadata={"type": "Attribute"})

    din_enclosure: DINEnclosure | None = field(
        default=None,
        metadata={
            "name": "DINEnclosure",
        },
    )
    module_count: int | None = None
