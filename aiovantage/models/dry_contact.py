from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from typing_extensions import override

from ..clients.hc import StatusType
from ..xml_dataclass import element_field
from .location_object import LocationObject

if TYPE_CHECKING:
    from .station import Station


@dataclass
class DryContact(LocationObject):
    station_id: Optional[int] = element_field(name="Parent", default=None)

    @override
    def status_handler(self, type: StatusType, args: Sequence[str]) -> None:
        # S:BTN {vid} {PRESS|RELEASE}
        state = args[0]

        self._logger.debug(
            f"DryContact state changed for {self.name} ({self.id}) to {state}"
        )

    @property
    def station(self) -> "Station | None":
        return self.vantage.stations.get(id=self.station_id)
