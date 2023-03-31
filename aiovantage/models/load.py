import shlex
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from typing_extensions import override

from ..clients.hc import StatusType
from .vantage_object import VantageObject
from .xml_model import attr, element

if TYPE_CHECKING:
    from .area import Area


def _parse_level(*args: str) -> float:
    return float(args[0])


@dataclass
class Load(VantageObject):
    id: int = attr(alias="VID")
    name: str | None = element(alias="Name", default=None)
    display_name: str | None = element(alias="DName", default=None)
    load_type: str | None = element(alias="LoadType", default=None)
    area_id: int | None = element(alias="Area", default=None)
    _level: float | None = None

    @override
    def status_handler(self, type: StatusType, args: Sequence[str]) -> None:
        # S:LOAD {vid} {level}
        level = _parse_level(*args)
        self._level = level

        self._logger.debug(f"Load level changed for {self.name} ({self.id}) to {level}")

    @property
    def area(self) -> "Area | None":
        return self.vantage.areas.get(id=self.area_id)

    async def get_level(self) -> float:
        message = await self.vantage._hc_client.send_command("GETLOAD", f"{self.id}")
        status_type, vid, *args = shlex.split(message[2:])
        level = _parse_level(*args)
        self._level = level

        return level

    async def set_level(self, value: float) -> None:
        value = max(min(value, 100), 0)
        await self.vantage._hc_client.send_command("LOAD", f"{self.id}", f"{value}")
        self._level = value
