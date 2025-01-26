"""Light sensor object."""

from dataclasses import dataclass, field
from decimal import Decimal

from .sensor import Sensor
from .types import Parent


@dataclass(kw_only=True)
class LightSensor(Sensor):
    """Light sensor object."""

    parent: Parent

    # State
    level: Decimal | None = field(default=None, metadata={"type": "Ignore"})
