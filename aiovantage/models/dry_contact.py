from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from typing_extensions import override

from aiovantage.clients.hc import StatusType
from aiovantage.models.location_object import LocationObject

if TYPE_CHECKING:
    from aiovantage.models.station import Station


@dataclass
class DryContact(LocationObject):
    station_id: Optional[int] = field(
        default=None,
        metadata=dict(
            type="Element",
            name="Parent",
        ),
    )

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
