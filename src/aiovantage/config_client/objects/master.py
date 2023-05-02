from dataclasses import dataclass

from aiovantage.config_client.xml_dataclass import xml_element

from .system_object import SystemObject


@dataclass
class Master(SystemObject):
    number: int = xml_element("Number")
    volts: float = xml_element("Volts")
    amps: float = xml_element("Amps")
    module_count: int = xml_element("ModuleCount")
    serial_number: int = xml_element("SerialNumber")
