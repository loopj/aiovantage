from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..xml_dataclass import element_field
from .system_object import SystemObject

if TYPE_CHECKING:
    from .area import Area


@dataclass
class LocationObject(SystemObject):
    """Base class for objects that have an Area."""

    area_id: int | None = element_field(name="Area", default=None)

    @property
    def area(self) -> "Area | None":
        return self.vantage.areas.get(id=self.area_id)
