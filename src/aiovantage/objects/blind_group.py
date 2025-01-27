"""BlindGroup object."""

from dataclasses import dataclass, field

from .blind_group_base import BlindGroupBase
from .location_object import LocationObject


@dataclass(kw_only=True)
class BlindGroup(BlindGroupBase, LocationObject):
    """BlindGroup object."""

    category: int
    blind_table: list[int] = field(
        default_factory=list,
        metadata={
            "name": "Blind",
            "wrapper": "BlindTable",
        },
    )
