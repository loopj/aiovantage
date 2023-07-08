"""Master (controller) object."""

from dataclasses import dataclass
from typing import Optional

from aiovantage.config_client.xml_dataclass import xml_element

from .system_object import SystemObject


@dataclass
class Master(SystemObject):
    """Master (controller) object."""

    number: int = xml_element("Number")
    volts: float = xml_element("Volts")
    amps: float = xml_element("Amps")
    module_count: int = xml_element("ModuleCount")
    serial_number: int = xml_element("SerialNumber")

    def __post_init__(self) -> None:
        """Post init hook."""
        self.last_updated: Optional[int] = None
        self.firmware_version: Optional[str] = None
