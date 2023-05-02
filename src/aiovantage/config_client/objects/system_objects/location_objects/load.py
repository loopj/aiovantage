from dataclasses import dataclass
from typing import Optional

from aiovantage.config_client.xml_dataclass import xml_element

from ..location_object import LocationObject


@dataclass
class Load(LocationObject):
    load_type: str = xml_element("LoadType")
    power_profile_id: int = xml_element("PowerProfile")

    @property
    def is_dimmable(self) -> bool:
        return not (
            self.load_type.endswith("non-Dim")
            or self.load_type == "High Voltage Relay"
            or self.load_type == "Low Voltage Relay"
        )

    def __post_init__(self) -> None:
        self.level: Optional[float] = None
