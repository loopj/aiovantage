"""Light sensor object."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from aiovantage.config_client.xml_dataclass import xml_element

from .sensor import Sensor


@dataclass
class LightSensor(Sensor):
    """Light sensor object."""

    parent_id: int = xml_element("Parent")

    def __post_init__(self) -> None:
        """Declare state attributes in post init."""
        self.level: Optional[Decimal] = None
