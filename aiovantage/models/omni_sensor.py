from dataclasses import dataclass
from typing import Optional

from .base import Base, xml_attr, xml_tag


@dataclass
class OmniSensor(Base):
    id: int = xml_attr("VID")
    name: Optional[str] = xml_tag("Name")
    display_name: Optional[str] = xml_tag("DName")
    _level: Optional[float] = None