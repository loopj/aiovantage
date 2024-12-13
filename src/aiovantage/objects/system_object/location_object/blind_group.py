"""BlindGroup object."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces.blind import BlindInterface

from . import LocationObject


@dataclass(kw_only=True)
class BlindGroup(LocationObject, BlindInterface):
    """BlindGroup object."""

    blind_table: list[int] = field(
        default_factory=list,
        metadata={
            "name": "Blind",
            "wrapper": "BlindTable",
        },
    )
