import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from .base import Base
from .utils import get_element_int, get_element_text

if TYPE_CHECKING:
    from .area import Area


@dataclass
class Load(Base):
    load_type: Optional[str] = None
    area_id: Optional[int] = None
    _level: Optional[float] = None

    @classmethod
    def from_xml(cls, el: ET.Element) -> "Load":
        obj = super().from_xml(el)
        obj.load_type = get_element_text(el, "LoadType")
        obj.area_id = get_element_int(el, "Area")
        return obj

    @property
    def area(self) -> Optional["Area"]:
        return self._vantage.areas.get(id=self.area_id)

    @property
    def level(self) -> Optional[float]:
        return self._level

    async def set_level(self, value: float) -> None:
        await self._vantage._commands_client.send_sync(f"LOAD {self.id} {value}")
        self._level = value