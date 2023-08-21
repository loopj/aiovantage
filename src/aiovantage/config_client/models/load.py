"""Load object."""

from typing import Optional

from attr import define, field

from .location_object import LocationObject
from .types import Parent


@define
class Load(LocationObject):
    """Load object."""

    parent: Parent = field(
        metadata={
            "name": "Parent",
        }
    )

    load_type: str = field(
        metadata={
            "name": "LoadType",
        }
    )

    power_profile_id: int = field(
        metadata={
            "name": "PowerProfile",
        }
    )

    level: Optional[float] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

    @property
    def is_relay(self) -> bool:
        """Return True if the load type is a relay."""
        return self.load_type in (
            "High Voltage Relay",
            "Low Voltage Relay",
        )

    @property
    def is_motor(self) -> bool:
        """Return True if the load type is a motor."""
        return self.load_type == "Motor"

    @property
    def is_light(self) -> bool:
        """Return True if the load type is inferred to be a light."""
        return not (self.is_relay or self.is_motor)

    @property
    def is_on(self) -> bool:
        """Return True if the load is on."""
        return bool(self.level)
