"""Blind base class."""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

from aiovantage.config_client.xml_dataclass import xml_attribute

from .system_object import SystemObject


@dataclass
class BlindBase(SystemObject):
    """Blind base class."""

    orientation: Optional[str] = xml_attribute("ShadeOrientation", default=None)
    type: Optional[str] = xml_attribute("ShadeType", default=None)

    def __post_init__(self) -> None:
        """Declare state attributes in post init."""
        self.position: Optional[Decimal] = None
