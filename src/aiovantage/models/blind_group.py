"""BlindGroup object."""

from dataclasses import dataclass, field

from aiovantage.models.location_object import LocationObject
from aiovantage.object_interfaces.blind import BlindInterface


@dataclass
class BlindGroup(LocationObject, BlindInterface):
    """BlindGroup object."""

    blind_ids: list[int] = field(
        default_factory=list,
        metadata={
            "name": "Blind",
            "wrapper": "BlindTable",
        },
    )
