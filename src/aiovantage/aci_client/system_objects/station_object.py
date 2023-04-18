from dataclasses import dataclass

from ..xml_dataclass import xml_element
from .location_object import LocationObject


@dataclass
class StationObject(LocationObject):
    serial_number: str = xml_element("SerialNumber")
    bus_id: int = xml_element("Bus")


@dataclass
class Keypad(StationObject):
    """Keypad Station"""
    pass


@dataclass
class Dimmer(StationObject):
    """ScenePoint Dimmer Station"""
    pass


@dataclass
class ScenePointRelay(StationObject):
    """ScenePoint Relay Station"""
    pass


@dataclass
class DualRelayStation(StationObject):
    """ScenePoint Dual Relay Station"""
    pass


@dataclass
class EqCtrl(StationObject):
    """Equinox 40 Station"""
    pass


@dataclass
class EqUX(StationObject):
    """Equinox 41 or Equinox 73"""
    pass
