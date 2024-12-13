"""BlindGroup object."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces.blind import BlindInterface
from aiovantage.objects.location_object import LocationObject


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
