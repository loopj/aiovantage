from .system_object import SystemObject
from .system_objects.button import Button
from .system_objects.gmem import GMem
from .system_objects.location_object import LocationObject
from .system_objects.location_objects.area import Area
from .system_objects.location_objects.dry_contact import DryContact
from .system_objects.location_objects.load import Load
from .system_objects.location_objects.rgb_load import RGBLoad
from .system_objects.location_objects.rgb_loads.dg_color_load import DGColorLoad
from .system_objects.location_objects.rgb_loads.ddg_color_load import DDGColorLoad
from .system_objects.location_objects.sensor import Sensor
from .system_objects.location_objects.sensors.anemo_sensor import AnemoSensor
from .system_objects.location_objects.sensors.light_sensor import LightSensor
from .system_objects.location_objects.sensors.omni_sensor import OmniSensor
from .system_objects.location_objects.sensors.temperature import Temperature
from .system_objects.location_objects.station_object import StationObject
from .system_objects.location_objects.station_objects.eq_ctrl import EqCtrl
from .system_objects.location_objects.station_objects.eq_ux import EqUX
from .system_objects.location_objects.station_objects.keypad import Keypad
from .system_objects.location_objects.station_objects.keypads.dimmer import Dimmer
from .system_objects.location_objects.station_objects.keypads.dual_relay_station import DualRelayStation # noqa: E501
from .system_objects.location_objects.station_objects.keypads.scene_point_relay import ScenePointRelay # noqa: E501
from .system_objects.master import Master
from .system_objects.power_profile import PowerProfile
from .system_objects.power_profiles.dc_power_profile import DCPowerProfile
from .system_objects.power_profiles.dc_power_profiles.pwm_power_profile import PWMPowerProfile # noqa: E501
from .system_objects.station_bus import StationBus
from .system_objects.task import Task

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