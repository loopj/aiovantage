"""Equinox 40 Station."""

from dataclasses import dataclass

from .station_object import StationObject


@dataclass(kw_only=True)
class EqCtrl(StationObject):
    """Equinox 40 Station."""
