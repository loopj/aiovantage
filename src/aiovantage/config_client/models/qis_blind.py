"""QIS blind object."""

from attr import define

from .blind_base import BlindBase
from .station_object import StationObject


@define
class QISBlind(BlindBase, StationObject):
    """QIS blind object."""
