"""Base class for DIN station objects."""

from dataclasses import dataclass, field

from .station_object import StationObject


@dataclass(kw_only=True)
class DINStation(StationObject):
    """Base class for DIN station objects."""

    @dataclass
    class Enclosure:
        enclosure: int = field(metadata={"type": "Text"})
        position: int = field(metadata={"type": "Attribute"})
        row: int = field(metadata={"type": "Attribute"})

    din_enclosure: Enclosure = field(metadata={"name": "DINEnclosure"})
    module_count: int
