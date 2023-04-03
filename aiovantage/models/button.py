from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from typing_extensions import override

from aiovantage.clients.hc import StatusType
from aiovantage.models.system_object import SystemObject
from aiovantage.xml_dataclass import element_field

if TYPE_CHECKING:
    from aiovantage.models.station import Station


@dataclass
class Button(SystemObject):
    text: Optional[str] = element_field(name="Text1", default=None)
    station_id: Optional[int] = element_field(name="Parent", default=None)

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
