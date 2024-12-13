"""Equinox 40 Station."""

from dataclasses import dataclass

from aiovantage.object_interfaces import SounderInterface

from . import StationObject


@dataclass(kw_only=True)
class EqCtrl(StationObject, SounderInterface):
    """Equinox 40 Station."""
