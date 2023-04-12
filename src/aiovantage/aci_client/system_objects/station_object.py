from dataclasses import dataclass
from typing import Optional

from ..xml_dataclass import xml_element
from .location_object import LocationObject


@dataclass
class StationObject(LocationObject):
    serial_number: Optional[str] = xml_element("SerialNumber", default=None)
    bus: Optional[int] = xml_element("Bus", default=None)


@dataclass
class Keypad(StationObject):
    pass


@dataclass
class Dimmer(StationObject):
    pass


@dataclass
class ScenePointRelay(StationObject):
    pass


@dataclass
class DualRelayStation(StationObject):
    pass


@dataclass
class EqCtrl(StationObject):
    pass


@dataclass
class EqUX(StationObject):
    pass
