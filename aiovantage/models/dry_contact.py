from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional

from .vantage_object import VantageObject
from .xml_model import xml_attr, xml_tag

if TYPE_CHECKING:
    from .area import Area
    from .station import Station


@dataclass
class DryContact(VantageObject):
    id: int = xml_attr("VID")
    name: Optional[str] = xml_tag("Name", default=None)
    display_name: Optional[str] = xml_tag("DName", default=None)
    area_id: Optional[int] = xml_tag("Area", default=None)
    station_id: Optional[int] = xml_tag("Parent", default=None)

    # S:BTN {vid} {PRESS|RELEASE}
    def status_handler(self, args: Any) -> None:
        state = args[0]

        self._logger.debug(
            f"DryContact state changed for {self.name} ({self.id}) to {state}"
        )

    @property
    def area(self) -> Optional["Area"]:
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage.areas.get(id=self.area_id)

    @property
    def station(self) -> Optional["Station"]:
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage.stations.get(id=self.station_id)
