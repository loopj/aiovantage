"""Vantage object types."""

from ._objects.anemo_sensor import AnemoSensor
from ._objects.area import Area
from ._objects.back_box import BackBox
from ._objects.blind import Blind
from ._objects.blind_group import BlindGroup
from ._objects.button import Button
from ._objects.child_device import ChildDevice
from ._objects.contact_input import ContactInput
from ._objects.custom_device import CustomDevice
from ._objects.dc_power_profile import DCPowerProfile
from ._objects.dimmer import Dimmer
from ._objects.din_contact_input import DINContactInput
from ._objects.din_low_voltage_relay_station import DINLowVoltageRelayStation
from ._objects.din_station import DINStation
from ._objects.dry_contact import DryContact
from ._objects.dual_relay_station import DualRelayStation
from ._objects.eq_ctrl import EqCtrl
from ._objects.eq_ux import EqUX
from ._objects.gmem import GMem
from ._objects.high_voltage_relay_station import HighVoltageRelayStation
from ._objects.keypad import Keypad
from ._objects.light_sensor import LightSensor
from ._objects.load import Load
from ._objects.load_group import LoadGroup
from ._objects.location_object import LocationObject
from ._objects.low_voltage_relay_station import LowVoltageRelayStation
from ._objects.master import Master
from ._objects.module import Module
from ._objects.module_gen2 import ModuleGen2
from ._objects.omni_sensor import OmniSensor
from ._objects.parent_device import ParentDevice
from ._objects.port_device import PortDevice
from ._objects.power_profile import PowerProfile
from ._objects.pwm_power_profile import PWMPowerProfile
from ._objects.qis_blind import QISBlind
from ._objects.qube_blind import QubeBlind
from ._objects.relay_blind import RelayBlind
from ._objects.rs232_station import RS232Station
from ._objects.rs485_station import RS485Station
from ._objects.scene_point_relay import ScenePointRelay
from ._objects.sensor import Sensor
from ._objects.somfy_rs_485_sdn_20 import (
    SomfyRS485GroupChild,
    SomfyRS485SDN20Port,
    SomfyRS485ShadeChild,
)
from ._objects.somfy_urtsi_2 import (
    SomfyURTSI2GroupChild,
    SomfyURTSI2Port,
    SomfyURTSI2ShadeChild,
)
from ._objects.station_bus import StationBus
from ._objects.station_object import StationObject
from ._objects.system_object import SystemObject
from ._objects.task import Task
from ._objects.temperature import Temperature
from ._objects.thermostat import Thermostat
from ._objects.types import Parent
from ._objects.vantage_ddg_color_load import VantageDDGColorLoad
from ._objects.vantage_dg_color_load import VantageDGColorLoad
from ._objects.vantage_dmx_dali_gateway import VantageDmxDaliGateway
from ._objects.vantage_dmx_gateway import VantageDmxGateway

__all__ = [
    "AnemoSensor",
    "Area",
    "BackBox",
    "Blind",
    "BlindGroup",
    "Button",
    "ChildDevice",
    "ContactInput",
    "CustomDevice",
    "DCPowerProfile",
    "Dimmer",
    "DINContactInput",
    "DINLowVoltageRelayStation",
    "DINStation",
    "DryContact",
    "DualRelayStation",
    "EqCtrl",
    "EqUX",
    "GMem",
    "HighVoltageRelayStation",
    "Keypad",
    "LightSensor",
    "Load",
    "LoadGroup",
    "LocationObject",
    "LowVoltageRelayStation",
    "Master",
    "Module",
    "ModuleGen2",
    "OmniSensor",
    "Parent",
    "ParentDevice",
    "PortDevice",
    "PowerProfile",
    "PWMPowerProfile",
    "QISBlind",
    "QubeBlind",
    "RelayBlind",
    "RS232Station",
    "RS485Station",
    "ScenePointRelay",
    "Sensor",
    "SomfyRS485GroupChild",
    "SomfyRS485SDN20Port",
    "SomfyRS485ShadeChild",
    "SomfyURTSI2GroupChild",
    "SomfyURTSI2Port",
    "SomfyURTSI2ShadeChild",
    "StationBus",
    "StationObject",
    "SystemObject",
    "Task",
    "Temperature",
    "Thermostat",
    "VantageDDGColorLoad",
    "VantageDGColorLoad",
    "VantageDmxDaliGateway",
    "VantageDmxGateway",
]
