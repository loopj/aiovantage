"""Temperature object."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from .child_object import ChildObject
from .sensor import Sensor


@dataclass
class Temperature(Sensor, ChildObject):
    """Temperature object."""

    def __post_init__(self) -> None:
        """Declare state attributes in post init."""
        self.value: Optional[Decimal] = None
