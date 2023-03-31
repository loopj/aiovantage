import shlex
from dataclasses import dataclass
from typing import TYPE_CHECKING

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

    # S:LOAD {vid} {level}
    def status_handler(self, args: list[str]) -> None:
        level = _parse_level(*args)
        self._level = level

        self._logger.debug(f"Load level changed for {self.name} ({self.id}) to {level}")

    @property
    def area(self) -> "Area | None":
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage.areas.get(id=self.area_id)

    async def get_level(self) -> float:
        if self._vantage is None:
            raise Exception("Vantage client not set")

        message = await self._vantage._hc_client.send_command("GETLOAD", f"{self.id}")
        status_type, vid, *args = shlex.split(message[2:])
        level = _parse_level(*args)
        self._level = level

        return level

    async def set_level(self, value: float) -> None:
        if self._vantage is None:
            raise Exception("Vantage client not set")

        value = max(min(value, 100), 0)
        await self._vantage._hc_client.send_command("LOAD", f"{self.id}", f"{value}")
        self._level = value

    # Home assistant defines things like
    #
    # turn_on(
    #   transition: int,
    #   brightness: int,
    #   hs_color: Tuple[float, float],
    #   rgb_color: Tuple[int, int, int]
    # )
    #
    # turn_off(
    #   transition: int
    # )
    #
    # toggle() # Same args as turn_on

    # Google home defines things like
    #
    # OnOff trait
    # Brightness trait
    # ColorSetting trait
