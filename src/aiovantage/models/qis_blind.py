"""QIS blind object."""

from dataclasses import dataclass

from aiovantage.models.station_object import StationObject
from aiovantage.object_interfaces.blind import BlindInterface


@dataclass
class QISBlind(StationObject, BlindInterface):
    """QIS blind object."""
