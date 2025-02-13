"""Vantage HVAC-IU objects."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces import FanInterface, ThermostatInterface

from .child_device import ChildDevice
from .port_device import PortDevice


@dataclass(kw_only=True)
class VantageHVACIUPort(PortDevice):
    """Vantage HVAC-IU port device."""

    class Meta:
        name = "Vantage.HVAC-IU_PORT"

    temperature_format: str = field(
        default="Celcius",  # NOTE: Intentional typo to match the underlying object
        metadata={"name": "aTemperatureFormat"},
    )
    outdoor_sensor: int
    pauze_time: int = 1  # NOTE: Intentional typo to match the underlying object
    serial_number: str = "0"


@dataclass(kw_only=True)
class VantageHVACIULineChild(ChildDevice):
    """Vantage HVAC-IU line child device."""

    class Meta:
        name = "Vantage.HVAC-IU-Line_CHILD"

    @dataclass(kw_only=True)
    class OperationModes:
        auto: bool = True
        cool: bool = True
        heat: bool = True

    @dataclass(kw_only=True)
    class FanSpeeds:
        auto: bool = True
        high: bool = True
        low: bool = True
        max: bool = True
        med: bool = True

    device_type: str = "Daikin"
    line_number: int = 1
    operation_modes: OperationModes
    fan_speeds: FanSpeeds = field(metadata={"name": "xFanSpeeds"})


@dataclass(kw_only=True)
class VantageHVACIUZoneChild(ChildDevice, ThermostatInterface, FanInterface):
    """Vantage HVAC-IU zone child device."""

    class Meta:
        name = "Vantage.HVAC-IU-Zone_CHILD"

    @dataclass(kw_only=True)
    class IndoorSensor:
        indoor_sensor: int
        indoor_temp_offset: str = "0"

    main_zone: str = field(
        metadata={"name": "ZoneNumber", "wrapper": "aMainZonePlaceHolder"}
    )

    grouped_zones: list[str] = field(
        default_factory=list,
        metadata={"name": "ZoneNumberChild", "wrapper": "bGroupZonePlaceHolder"},
    )

    indoor_sensors: list[IndoorSensor] = field(
        default_factory=list, metadata={"name": "cIndoorSensors"}
    )
