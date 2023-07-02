"""Base class for all station objects."""

from dataclasses import dataclass

from aiovantage.config_client.xml_dataclass import xml_element

from .location_object import LocationObject


@dataclass
class StationObject(LocationObject):
    """Base class for all station objects."""

    serial_number: str = xml_element("SerialNumber")
    position: int = xml_element("Position")
    bus_id: int = xml_element("Bus")
