"""OmniSensor object."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Union

from aiovantage.config_client.xml_dataclass import xml_attribute, xml_element

from .sensor import Sensor


@dataclass
class OmniSensor(Sensor):
    """OmniSensor object."""

    @dataclass
    class GetMethodType:
        """Omnisensor method information."""

        @dataclass
        class Formula:
            """OmniSensor type conversion information."""

            return_type: str = xml_attribute("ReturnType")
            level_type: str = xml_attribute("LevelType")

        formula: Formula = xml_element("Formula")
        method: str = xml_element("Method")
        method_hw: str = xml_element("MethodHW")

    get: GetMethodType = xml_element("Get")
    parent_id: int = xml_element("Parent")

    def __post_init__(self) -> None:
        """Post init."""
        self.level: Union[int, Decimal, None] = None

    @property
    def is_current_sensor(self) -> bool:
        """Return True if the sensor is a current sensor."""
        return self.model == "Current"

    @property
    def is_power_sensor(self) -> bool:
        """Return True if the sensor is a power sensor."""
        return self.model == "Power"

    @property
    def is_temperature_sensor(self) -> bool:
        """Return True if the sensor is a temperature sensor."""
        return self.model == "Temperature"
