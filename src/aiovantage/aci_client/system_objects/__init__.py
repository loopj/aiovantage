from .area import Area
from .button import Button
from .dry_contact import DryContact
from .gmem import GMem
from .load import Load
from .location_object import LocationObject
from .power_profile import PowerProfile, DCPowerProfile, PWMPowerProfile
from .rgb_load import RGBLoad, DGColorLoad, DDGColorLoad
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

# Concrete Sensor classes
SENSOR_TYPES = [
    AnemoSensor,
    LightSensor,
    OmniSensor,
    Temperature,
]

# Concrete StationObject classes
STATION_TYPES = [
    Dimmer,
    DualRelayStation,
    EqCtrl,
    EqUX,
    Keypad,
    ScenePointRelay,
]

# Concrete PowerProfile classes
POWER_PROFILES = [
    PowerProfile,
    DCPowerProfile,
    PWMPowerProfile,
]

# Concrete RGBLoad classes
COLOR_LOADS = [
    DGColorLoad,
    DDGColorLoad,
]

ALL_TYPES = (
    [
        Area,
        Button,
        DryContact,
        GMem,
        Load,
        LocationObject,
        RGBLoad,
        Sensor,
        StationBus,
        StationObject,
        SystemObject,
        Task,
    ]
    + COLOR_LOADS
    + POWER_PROFILES
    + STATION_TYPES
    + SENSOR_TYPES
)

__all__ = [obj.__name__ for obj in ALL_TYPES]
