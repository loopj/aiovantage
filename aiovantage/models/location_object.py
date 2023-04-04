from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from aiovantage.models.system_object import SystemObject

if TYPE_CHECKING:
    from aiovantage.models.area import Area


@dataclass
class LocationObject(SystemObject):
    """Base class for objects that have an Area."""

    area_id: Optional[int] = field(
        default=None,
        metadata=dict(
            type="Element",
            name="Area",
        ),
    )

    @property
    def area(self) -> "Area | None":
        return self.vantage.areas.get(id=self.area_id)
