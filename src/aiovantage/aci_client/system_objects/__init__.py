from .area import Area
from .button import Button
from .dry_contact import DryContact
from .gmem import GMem
from .load import Load
from .location_object import LocationObject
from .sensor import AnemoSensor, LightSensor, OmniSensor, Sensor, Temperature
from .station_bus import StationBus
from .station_object import (
    Dimmer,
    DualRelayStation,
    EqCtrl,
    EqUX,
    Keypad,
    ScenePointRelay,
    StationObject,
)
from .system_object import SystemObject
from .task import Task

SENSOR_TYPES = [
    AnemoSensor,
    LightSensor,
    OmniSensor,
    Temperature,
]

STATION_TYPES = [
    Dimmer,
    DualRelayStation,
    EqCtrl,
    EqUX,
    Keypad,
    ScenePointRelay,
]

ALL_TYPES = (
    [
        Area,
        Button,
        DryContact,
        GMem,
        Load,
        LocationObject,
        Sensor,
        StationBus,
        StationObject,
        SystemObject,
        Task,
    ]
    + STATION_TYPES
    + SENSOR_TYPES
)

__all__ = [obj.__name__ for obj in ALL_TYPES]
