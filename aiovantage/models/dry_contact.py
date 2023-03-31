from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from typing_extensions import override

from ..clients.hc import StatusType
from .vantage_object import VantageObject
from .xml_model import attr, element

if TYPE_CHECKING:
    from .area import Area
    from .station import Station


@dataclass
class DryContact(VantageObject):
    id: int = attr(alias="VID")
    name: str | None = element(alias="Name", default=None)
    display_name: str | None = element(alias="DName", default=None)
    area_id: int | None = element(alias="Area", default=None)
    station_id: int | None = element(alias="Parent", default=None)

    @override
    def status_handler(self, type: StatusType, args: Sequence[str]) -> None:
        # S:BTN {vid} {PRESS|RELEASE}
        state = args[0]

        self._logger.debug(
            f"DryContact state changed for {self.name} ({self.id}) to {state}"
        )

    @property
    def area(self) -> "Area | None":
        return self.vantage.areas.get(id=self.area_id)

    @property
    def station(self) -> "Station | None":
        return self.vantage.stations.get(id=self.station_id)
