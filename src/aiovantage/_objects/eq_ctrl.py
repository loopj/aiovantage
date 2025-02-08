"""Equinox 40 Station."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces import SounderInterface

from .station_object import StationObject


@dataclass(kw_only=True)
class EqCtrl(StationObject, SounderInterface):
    """Equinox 40 Station."""

    @dataclass
    class Header:
        object: int
        type: str = field(metadata={"type": "Attribute"})

    pages: int
    activate: int
    style: int
    header: Header
    zone: int
    preset_table: list[int] = field(
        default_factory=list,
        metadata={
            "name": "Preset",
            "wrapper": "PresetTable",
        },
    )
