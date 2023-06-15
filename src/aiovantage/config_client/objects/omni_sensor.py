from dataclasses import dataclass

from aiovantage.config_client.xml_dataclass import xml_attribute, xml_element

from .sensor import Sensor


@dataclass
class OmniSensor(Sensor):
    @dataclass
    class GetMethodType:
        @dataclass
        class Formula:
            return_type: str = xml_attribute("ReturnType")
            level_type: str = xml_attribute("LevelType")

        formula: Formula = xml_element("Formula")
        method: str = xml_element("Method")
        method_hw: str = xml_element("MethodHW")

    get: GetMethodType = xml_element("Get")
    parent_id: int = xml_element("Parent")

    @property
    def is_current_sensor(self) -> bool:
        return self.model == "Current"

    @property
    def is_power_sensor(self) -> bool:
        return self.model == "Power"

    @property
    def is_temperature_sensor(self) -> bool:
        return self.model == "Temperature"
