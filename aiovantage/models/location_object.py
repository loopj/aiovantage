from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from aiovantage.models.system_object import SystemObject
from aiovantage.xml_dataclass import element_field

if TYPE_CHECKING:
    from aiovantage.models.area import Area


@dataclass
class LocationObject(SystemObject):
    """Base class for objects that have an Area."""

    area_id: Optional[int] = element_field(name="Area", default=None)

    @property
    def area(self) -> "Area | None":
        return self.vantage.areas.get(id=self.area_id)
