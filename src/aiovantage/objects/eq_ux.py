"""Equinox 41 or Equinox 73 touchscreen."""

from dataclasses import dataclass, field

from .station_object import StationObject


@dataclass(kw_only=True)
class EqUX(StationObject):
    """Equinox 41 or Equinox 73 touchscreen."""

    style: int
    profile_table: list[int] = field(
        default_factory=list,
        metadata={
            "name": "Profile",
            "wrapper": "ProfileTable",
        },
    )
    activate: int
