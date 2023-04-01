from dataclasses import dataclass
from typing import TYPE_CHECKING

from .system_object import SystemObject
from ..xml_dataclass import element_field

if TYPE_CHECKING:
    from .area import Area


@dataclass
class LocationObject(SystemObject):
    area_id: int | None = element_field(name="Area", default=None)

    @property
    def area(self) -> "Area | None":
        return self.vantage.areas.get(id=self.area_id)
