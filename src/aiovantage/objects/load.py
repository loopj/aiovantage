"""Load object."""

from dataclasses import dataclass
from decimal import Decimal

from aiovantage.object_interfaces import LoadInterface

from .location_object import LocationObject
from .types import Parent


@dataclass(kw_only=True)
class Load(LocationObject, LoadInterface):
    """Load object."""

    parent: Parent
    contractor_number: str
    load_type: str = "Incandescent"
    power: int = 100
    power_profile: int
    override_level: Decimal = Decimal("100")

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

    @property
    def is_on(self) -> bool:
        """Return True if the load is on."""
        return bool(self.level)
