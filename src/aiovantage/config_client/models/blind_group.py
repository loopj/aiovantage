"""BlindGroup object."""

from dataclasses import dataclass, field
from typing import List

from .blind_group_base import BlindGroupBase
from .location_object import LocationObject


@dataclass
class BlindGroup(BlindGroupBase, LocationObject):
    """BlindGroup object."""

    blind_ids: List[int] = field(
        metadata={
            "name": "Blind",
            "wrapper": "BlindTable",
        },
    )
