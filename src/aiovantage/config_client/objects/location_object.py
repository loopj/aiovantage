"""Base class for system objects in an area."""

from dataclasses import dataclass

from aiovantage.config_client.xml_dataclass import xml_element

from .system_object import SystemObject


@dataclass
class LocationObject(SystemObject):
    """Base class for system objects in an area."""

    area_id: int = xml_element("Area")
    location: str = xml_element("Location")
