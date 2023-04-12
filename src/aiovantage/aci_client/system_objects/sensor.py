from dataclasses import dataclass

from .location_object import LocationObject


@dataclass
class Sensor(LocationObject):
    pass


@dataclass
class OmniSensor(Sensor):
    pass


@dataclass
class LightSensor(Sensor):
    pass


@dataclass
class AnemoSensor(Sensor):
    pass


@dataclass
class Temperature(Sensor):
    pass
