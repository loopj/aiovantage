from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from .base import Base

if TYPE_CHECKING:
    from .station import Station


@dataclass
class Button(Base):
    id: int
    name: Optional[str] = None
    display_name: Optional[str] = None
    text: Optional[str] = None
    station_id: Optional[int] = None

    @property
    def station(self) -> Optional["Station"]:
        return self._vantage.stations.get(id=self.station_id)
