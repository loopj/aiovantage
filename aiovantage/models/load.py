import shlex
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Optional

from typing_extensions import override

from aiovantage.hc_client import StatusType
from aiovantage.models.location_object import LocationObject


def _parse_level(*args: str) -> float:
    return float(args[0])


@dataclass
class Load(LocationObject):
    load_type: Optional[str] = field(
        default=None,
        metadata=dict(
            type="Element",
            name="LoadType",
        ),
    )

    def __post_init__(self) -> None:
        self._level: Optional[float] = None

    @override
    def status_handler(self, type: StatusType, args: Sequence[str]) -> None:
        # S:LOAD {vid} {level}
        level = _parse_level(*args)
        self._level = level

        self._logger.debug(f"Load level changed for {self.name} ({self.id}) to {level}")

    @property
    def level(self) -> Optional[float]:
        return self._level

    async def get_level(self) -> float:
        message = await self.vantage._hc_client.send_command("GETLOAD", f"{self.id}")
        status_type, vid, *args = shlex.split(message)
        level = _parse_level(*args)
        self._level = level

        return level

    async def set_level(self, value: float) -> None:
        # Normalize level to 0-100
        value = max(min(value, 100), 0)

        # Check if level is already set to value
        if self._level == value:
            return

        # Send command to controller
        await self.vantage._hc_client.send_command("LOAD", f"{self.id}", f"{value}")

        # Update local level
        self._level = value

    async def turn_off(self) -> None:
        await self.set_level(0)

    async def turn_on(self) -> None:
        await self.set_level(100)
