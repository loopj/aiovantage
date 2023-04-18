from dataclasses import dataclass

from ..xml_dataclass import xml_element
from .system_object import SystemObject


@dataclass
class PowerProfile(SystemObject):
    min: float = xml_element("Min")
    max: float = xml_element("Max")
    adjust: int = xml_element("Adjust")
    freq: int = xml_element("Freq")
    inductive: bool = xml_element("Inductive")


@dataclass
class DCPowerProfile(PowerProfile):
    pass


@dataclass
class PWMPowerProfile(PowerProfile):
    pass
