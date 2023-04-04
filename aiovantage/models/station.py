from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from aiovantage.models.location_object import LocationObject
from aiovantage.query import QuerySet

if TYPE_CHECKING:
    from aiovantage.models.button import Button
    from aiovantage.models.dry_contact import DryContact


@dataclass
class Station(LocationObject):
    bus_id: Optional[int] = field(
        default=None,
        metadata=dict(
            type="Element",
            name="Bus",
        ),
    )

    @property
    def buttons(self) -> QuerySet["Button"]:
        return self.vantage.buttons.filter(station_id=self.id)

    @property
    def dry_contacts(self) -> QuerySet["DryContact"]:
        return self.vantage.dry_contacts.filter(station_id=self.id)
