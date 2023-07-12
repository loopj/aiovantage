"""Temperature object."""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from .child_object import ChildObject
from .sensor import Sensor


@dataclass
class Temperature(ChildObject, Sensor):
    """Temperature object."""

    value: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )
