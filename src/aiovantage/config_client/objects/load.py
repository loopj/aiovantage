"""Load object."""

from dataclasses import dataclass
from typing import Optional

from aiovantage.config_client.xml_dataclass import xml_element

from .location_object import LocationObject


@dataclass
class Load(LocationObject):
    """Load object."""

    load_type: str = xml_element("LoadType")
    parent_id: int = xml_element("Parent")
    power_profile_id: int = xml_element("PowerProfile")

    def __post_init__(self) -> None:
        """Declare state attributes in post init."""
        self.level: Optional[float] = None

    @property
    def is_relay(self) -> bool:
        """Return True if the load is a relay."""
        return self.load_type in (
            "High Voltage Relay",
            "Low Voltage Relay",
        )

    @property
    def is_motor(self) -> bool:
        """Return True if the load is a motor."""
        return self.load_type == "Motor"

    @property
    def is_light(self) -> bool:
        """Return True if the load is a light."""
        return not (self.is_relay or self.is_motor)

    @property
    def is_dimmable(self) -> bool:
        """Return True if the load is dimmable."""
        return not self.load_type.endswith("non-Dim")

    @property
    def is_on(self) -> bool:
        """Return True if the load is on."""
        return bool(self.level)
