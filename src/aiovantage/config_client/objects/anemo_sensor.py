"""AnemoSensor (wind sensor) object."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from aiovantage.config_client.xml_dataclass import xml_element

from .sensor import Sensor


@dataclass
class AnemoSensor(Sensor):
    """AnemoSensor (wind sensor) object."""

    parent_id: int = xml_element("Parent")

    def __post_init__(self) -> None:
        """Declare state attributes in post init."""
        self.speed: Optional[Decimal] = None
