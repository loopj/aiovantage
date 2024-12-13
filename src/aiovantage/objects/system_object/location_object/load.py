"""Load object."""

from dataclasses import dataclass

from aiovantage.object_interfaces.load import LoadInterface
from aiovantage.objects.types import Parent

from . import LocationObject


@dataclass(kw_only=True)
class Load(LocationObject, LoadInterface):
    """Load object."""

    parent: Parent
    load_type: str = "Incandescent"
    power_profile: int

    @property
    def is_relay(self) -> bool:
        """Return True if the load type is a relay."""
        return self.load_type in (
            "High Voltage Relay",
            "Low Voltage Relay",
            "[MDR8RW101]",
        )

    @property
    def is_motor(self) -> bool:
        """Return True if the load type is a motor."""
        return self.load_type == "Motor"

    @property
    def is_light(self) -> bool:
        """Return True if the load type is inferred to be a light."""
        return not (self.is_relay or self.is_motor)
