"""QIS blind object."""

from dataclasses import dataclass

from aiovantage.object_interfaces.blind import BlindInterface
from aiovantage.objects.station_object import StationObject


@dataclass
class QISBlind(StationObject, BlindInterface):
    """QIS blind object."""
