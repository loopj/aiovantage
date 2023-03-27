from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from .base import Base

if TYPE_CHECKING:
    from .area import Area


@dataclass
class Load(Base):
    id: int
    name: Optional[str] = None
    display_name: Optional[str] = None
    load_type: Optional[str] = None
    area_id: Optional[int] = None
    _level: Optional[float] = None

    @property
    def area(self) -> Optional["Area"]:
        return self._vantage.areas.get(id=self.area_id)

    @property
    def level(self) -> Optional[float]:
        return self._level

    async def set_level(self, value: float) -> None:
        await self._vantage._commands_client.send_sync(f"LOAD {self.id} {value}")
        self._level = value