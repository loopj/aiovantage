"""AnemoSensor (wind sensor) object."""

from dataclasses import dataclass, field
from decimal import Decimal

from .sensor import Sensor
from .types import Parent


@dataclass(kw_only=True)
class AnemoSensor(Sensor):
    """AnemoSensor (wind sensor) object."""

    parent: Parent
    out_of_range: int = 0
    in_range: int = 0
    range_high: float = 10.0
    range_low: float = 0.0
    hold_on_time: float

    # State
    speed: Decimal | None = field(default=None, metadata={"type": "Ignore"})
