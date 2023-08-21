"""BlindGroup object."""

from typing import List

from attr import define, field

from .blind_group_base import BlindGroupBase
from .location_object import LocationObject


@define
class BlindGroup(BlindGroupBase, LocationObject):
    """BlindGroup object."""

    blind_ids: List[int] = field(
        metadata={
            "name": "Blind",
            "wrapper": "BlindTable",
        },
    )
