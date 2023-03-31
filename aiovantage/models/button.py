from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from typing_extensions import override

from ..clients.hc import StatusType
from .vantage_object import VantageObject
from .xml_model import attr, element

if TYPE_CHECKING:
    from .station import Station


@dataclass
class Button(VantageObject):
    id: int = attr(alias="VID")
    name: str | None = element(alias="Name", default=None)
    display_name: str | None = element(alias="DName", default=None)
    text: str | None = element(alias="Text1", default=None)
    station_id: int | None = element(alias="Parent", default=None)

    @override
    def status_handler(self, type: StatusType, args: Sequence[str]) -> None:
        # S:BTN {vid} {PRESS|RELEASE}
        state = args[0]

        self._logger.debug(
            f"Button state changed for {self.name} {self.text} ({self.id}) to {state}"
        )

    @property
    def station(self) -> "Station | None":
        return self.vantage.stations.get(id=self.station_id)
