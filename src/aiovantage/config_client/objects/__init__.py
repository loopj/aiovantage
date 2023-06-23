"""Vantage object types."""

from .anemo_sensor import AnemoSensor
from .area import Area
from .blind import Blind
from .blind_group import BlindGroup
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
from .load_group import LoadGroup
from .location_object import LocationObject
from .master import Master
from .omni_sensor import OmniSensor
from .power_profile import PowerProfile
from .pwm_power_profile import PWMPowerProfile
from .qis_blind import QISBlind
from .qube_blind import QubeBlind
from .relay_blind import RelayBlind
from .rgb_load import RGBLoad
from .scene_point_relay import ScenePointRelay
from .sensor import Sensor
from .somfy.rs485_group import RS485Group
from .somfy.rs485_shade import RS485Shade
from .somfy.urtsi_2_group import URTSI2Group
from .somfy.urtsi_2_shade import URTSI2Shade
from .station_bus import StationBus
from .station_object import StationObject
from .system_object import SystemObject
from .task import Task
from .temperature import Temperature

__all__ = [
    "AnemoSensor",
    "Area",
    "Blind",
    "BlindGroup",
    "Button",
    "DCPowerProfile",
    "DDGColorLoad",
    "DGColorLoad",
    "Dimmer",
    "DryContact",
    "DualRelayStation",
    "EqCtrl",
    "EqUX",
    "GMem",
    "Keypad",
    "LightSensor",
    "Load",
    "LoadGroup",
    "LocationObject",
    "Master",
    "OmniSensor",
    "PowerProfile",
    "PWMPowerProfile",
    "QISBlind",
    "QubeBlind",
    "RelayBlind",
    "RGBLoad",
    "RS485Group",
    "RS485Shade",
    "ScenePointRelay",
    "Sensor",
    "StationBus",
    "StationObject",
    "SystemObject",
    "Task",
    "Temperature",
    "URTSI2Group",
    "URTSI2Shade",
]
