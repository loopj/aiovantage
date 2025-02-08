"""BlindGroup object."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces import BlindInterface

from .location_object import LocationObject


@dataclass(kw_only=True)
class BlindGroup(LocationObject, BlindInterface):
    """BlindGroup object."""

    category: int
    blind_table: list[int] = field(
        default_factory=list,
        metadata={
            "name": "Blind",
            "wrapper": "BlindTable",
        },
    )
