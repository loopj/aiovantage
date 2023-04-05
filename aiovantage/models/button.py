from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from typing_extensions import override

from aiovantage.hc_client import StatusType
from aiovantage.models.system_object import SystemObject

if TYPE_CHECKING:
    from aiovantage.models.station import Station


@dataclass
class Button(SystemObject):
    text: Optional[str] = field(
        default=None,
        metadata=dict(
            type="Element",
            name="Text1",
        ),
    )

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
            f"Button state changed for {self.name} {self.text} ({self.id}) to {state}"
        )

    @property
    def station(self) -> "Station | None":
        return self.vantage.stations.get(id=self.station_id)
