"""BlindGroup object."""

from dataclasses import dataclass, field

from .blind_group_base import BlindGroupBase
from .location_object import LocationObject


@dataclass
class BlindGroup(BlindGroupBase, LocationObject):
    """BlindGroup object."""

    blind_ids: list[int] = field(
        default_factory=list,
        metadata={
            "name": "Blind",
            "wrapper": "BlindTable",
        },
    )
