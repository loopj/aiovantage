"""Temperature object."""

from decimal import Decimal
from typing import Optional

from attr import define, field

from .sensor import Sensor
from .types import Parent


@define
class Temperature(Sensor):
    """Temperature object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )

    value: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )
