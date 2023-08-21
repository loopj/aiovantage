"""Temperature object."""

from decimal import Decimal
from typing import Optional

from attr import define, field

from .child_object import ChildObject
from .sensor import Sensor


@define
class Temperature(ChildObject, Sensor):
    """Temperature object."""

    value: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )
