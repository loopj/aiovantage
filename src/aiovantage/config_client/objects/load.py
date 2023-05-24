from dataclasses import dataclass
from typing import Optional

from aiovantage.config_client.xml_dataclass import xml_element

from .location_object import LocationObject

# Load types:
#   Cold Cathode
#   Electronic Low Voltage
#   Fluor. Electronic Dim
#   Fluor. Electronic non-Dim
#   Halogen
#   HID
#   High Voltage Relay
#   Incandescent
#   LED Dim
#   LED non-Dim
#   Low Voltage Relay
#   Magnetic Low Voltage
#   Motor

@dataclass
class Load(LocationObject):
    load_type: str = xml_element("LoadType")
    power_profile_id: int = xml_element("PowerProfile")

    @property
    def is_relay(self) -> bool:
        return self.load_type in (
            "High Voltage Relay",
            "Low Voltage Relay",
        )

    @property
    def is_motor(self) -> bool:
        return self.load_type == "Motor"

    @property
    def is_light(self) -> bool:
        return not (self.is_relay or self.is_motor)

    @property
    def is_dimmable(self) -> bool:
        return not self.load_type.endswith("non-Dim")

    def __post_init__(self) -> None:
        self.level: Optional[float] = None
