from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional

from .vantage_object import VantageObject
from .xml_model import xml_attr, xml_tag

if TYPE_CHECKING:
    from .station import Station


@dataclass
class Button(VantageObject):
    id: int = xml_attr("VID")
    name: Optional[str] = xml_tag("Name")
    display_name: Optional[str] = xml_tag("DName")
    text: Optional[str] = xml_tag("Text1")
    station_id: Optional[int] = xml_tag("Parent")

    # S:BTN {vid} {PRESS|RELEASE}
    def status_handler(self, args: Any) -> None:
        state = args[0]

        self._logger.debug(
            f"Button state changed for {self.name} {self.text} ({self.id}) to {state}"
        )

    @property
    def station(self) -> Optional["Station"]:
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage.stations.get(id=self.station_id)
