"""Temperature object."""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from .sensor import Sensor
from .types import Parent


@dataclass
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
