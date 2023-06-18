"""Power profile object."""

from dataclasses import dataclass

from aiovantage.config_client.xml_dataclass import xml_element

from .system_object import SystemObject


@dataclass
class PowerProfile(SystemObject):
    """Power Profile object."""

    min: float = xml_element("Min")
    max: float = xml_element("Max")
    adjust: int = xml_element("Adjust")
    freq: int = xml_element("Freq")
    inductive: bool = xml_element("Inductive")
