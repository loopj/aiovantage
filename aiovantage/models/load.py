import shlex
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional

from .vantage_object import VantageObject
from .xml_model import xml_attr, xml_tag

if TYPE_CHECKING:
    from .area import Area


def _parse_level(*args: str) -> float:
    return float(args[0])


@dataclass
class Load(VantageObject):
    id: int = xml_attr("VID")
    name: Optional[str] = xml_tag("Name")
    display_name: Optional[str] = xml_tag("DName")
    load_type: Optional[str] = xml_tag("LoadType")
    area_id: Optional[int] = xml_tag("Area")
    _level: Optional[float] = None

    # S:LOAD {vid} {level}
    def status_handler(self, args: Any) -> None:
        level = _parse_level(*args)
        self._level = level

        self._logger.debug(f"Load level changed for {self.name} ({self.id}) to {level}")

    @property
    def area(self) -> Optional["Area"]:
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage.areas.get(id=self.area_id)

    async def get_level(self) -> float:
        if self._vantage is None:
            raise Exception("Vantage client not set")

        message = await self._vantage._commands_client.send_sync(f"GETLOAD {self.id}")
        status_type, vid, *args = shlex.split(message[2:])
        level = _parse_level(*args)
        self._level = level

        return level

    async def set_level(self, value: float) -> None:
        if self._vantage is None:
            raise Exception("Vantage client not set")

        value = max(min(value, 100), 0)
        await self._vantage._commands_client.send_sync(f"LOAD {self.id} {value}")
        self._level = value
