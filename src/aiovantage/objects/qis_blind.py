"""QIS blind object."""

from dataclasses import dataclass

from aiovantage.object_interfaces import BlindInterface

from .station_object import StationObject


@dataclass
class QISBlind(StationObject, BlindInterface):
    """QIS blind object."""
