"""Vantage Generic HVAC RS485 objects."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces import FanInterface, ThermostatInterface

from .child_device import ChildDevice
from .port_device import PortDevice


@dataclass(kw_only=True)
class VantageGenericHVACRS485Port(PortDevice):
    """Vantage Generic HVAC RS485 port device."""

    class Meta:
        name = "Vantage.Generic_HVAC_RS485_PORT"

    @dataclass(kw_only=True)
    class FanSpeedSettings:
        auto_fan: bool = True
        high_fan: bool = True
        low_fan: bool = True
        max_fan: bool = True
        med_fan: bool = True
        off_fan: bool = True

    @dataclass(kw_only=True)
    class SensorSettings:
        no_device_sensors: bool = False
        outdoor_sensor: int = field(metadata={"name": "outdoorSensor"})
        outdoor_temp_offset: str = field(
            default="0", metadata={"name": "outdoorTempOffset"}
        )
        track_sensors: bool = False

    @dataclass(kw_only=True)
    class SetpointSettings:
        bind_setpoints: bool = False
        max_temp: int = 25
        min_temp: int = 15

    fan_boost_option: bool = False
    fan_speed_settings: FanSpeedSettings
    fan_individual_control: bool = False
    receive_port: int
    sensor_settings: SensorSettings
    setpoint_settings: SetpointSettings


@dataclass(kw_only=True)
class VantageGenericHVACRS485TechContactsChild(ChildDevice):
    """Vantage Generic HVAC RS485 tech contacts child device."""

    class Meta:
        name = "Vantage.Generic_HVAC_RS485_TechContacts_CHILD"


@dataclass(kw_only=True)
class VantageGenericHVACRS485CompoundChild(ChildDevice, ThermostatInterface):
    """Vantage Generic HVAC RS485 compound child device."""

    class Meta:
        name = "Vantage.Generic_HVAC_RS485_Compound_CHILD"

    adress_number: int = 1  # NOTE: Intentional typo to match the underlying object


@dataclass(kw_only=True)
class VantageGenericHVACRS485ZoneChild(ChildDevice, ThermostatInterface, FanInterface):
    """Vantage Generic HVAC RS485 zone child device."""

    class Meta:
        name = "Vantage.Generic_HVAC_RS485_Zone_CHILD"

    @dataclass(kw_only=True)
    class IndoorSettings:
        indoor_sensor: int = field(metadata={"name": "indoorSensor"})
        indoor_temp_offset: str = "0"

    indoor_settings: IndoorSettings
    position_number: int = 1


@dataclass(kw_only=True)
class VantageGenericHVACRS485ZoneWithoutFanSpeedChild(
    ChildDevice, ThermostatInterface, FanInterface
):
    """Vantage Generic HVAC RS485 zone child device without fan speed."""

    class Meta:
        name = "Vantage.Generic_HVAC_RS485_Zone_without_FanSpeed_CHILD"

    @dataclass(kw_only=True)
    class IndoorSettings:
        indoor_sensor: int = field(metadata={"name": "indoorSensor"})
        indoor_temp_offset: str = "0"

    indoor_settings: IndoorSettings
    position_number: int = 1
