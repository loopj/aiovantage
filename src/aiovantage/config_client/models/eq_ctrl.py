"""Equinox 40 Station."""

from attr import define

from .station_object import StationObject


@define
class EqCtrl(StationObject):
    """Equinox 40 Station."""
