from dataclasses import dataclass

from aiovantage.config_client.xml_dataclass import xml_element

from .location_object import LocationObject


@dataclass
class StationObject(LocationObject):
    serial_number: str = xml_element("SerialNumber")
    bus_id: int = xml_element("Bus")
