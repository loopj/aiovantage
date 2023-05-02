from .area import Area
from .button import Button
from .dry_contact import DryContact
from .gmem import GMem
from .load import Load
from .location_object import LocationObject
from .master import Master
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

# All concrete types (types that can appear in XML)
CONCRETE_TYPES = [
    # General
    Area,
    Button,
    DryContact,
    GMem,
    Load,
    Master,
    StationBus,
    Task,
    # Sensors
    AnemoSensor,
    LightSensor,
    OmniSensor,
    Temperature,
    # Stations
    Dimmer,
    DualRelayStation,
    EqCtrl,
    EqUX,
    Keypad,
    ScenePointRelay,
    # Power Profiles
    PowerProfile,
    DCPowerProfile,
    PWMPowerProfile,
    # RGB Loads
    DGColorLoad,
    DDGColorLoad,
]

# All types for export
ALL_TYPES = [
    LocationObject,
    RGBLoad,
    Sensor,
    StationObject,
    SystemObject,
] + CONCRETE_TYPES

__all__ = [obj.__name__ for obj in ALL_TYPES]
