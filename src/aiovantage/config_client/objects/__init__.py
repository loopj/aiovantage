from .anemo_sensor import AnemoSensor
from .area import Area
from .button import Button
from .dc_power_profile import DCPowerProfile
from .ddg_color_load import DDGColorLoad
from .dg_color_load import DGColorLoad
from .dimmer import Dimmer
from .dry_contact import DryContact
from .dual_relay_station import DualRelayStation
from .eq_ctrl import EqCtrl
from .eq_ux import EqUX
from .gmem import GMem
from .keypad import Keypad
from .light_sensor import LightSensor
from .load import Load
from .location_object import LocationObject
from .master import Master
from .omni_sensor import OmniSensor
from .power_profile import PowerProfile
from .pwm_power_profile import PWMPowerProfile
from .rgb_load import RGBLoad
from .scene_point_relay import ScenePointRelay
from .sensor import Sensor
from .station_bus import StationBus
from .station_object import StationObject
from .system_object import SystemObject
from .task import Task
from .temperature import Temperature

ALL_OBJECT_TYPES = (
    AnemoSensor,
    Area,
    Button,
    DCPowerProfile,
    DDGColorLoad,
    DGColorLoad,
    Dimmer,
    DryContact,
    DualRelayStation,
    EqCtrl,
    EqUX,
    GMem,
    Keypad,
    LightSensor,
    Load,
    LocationObject,
    Master,
    OmniSensor,
    PowerProfile,
    PWMPowerProfile,
    RGBLoad,
    ScenePointRelay,
    Sensor,
    StationBus,
    StationObject,
    SystemObject,
    Task,
    Temperature,
)

__all__ = [obj.__name__ for obj in ALL_OBJECT_TYPES]
