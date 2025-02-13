"""Vantage Virtual Thermostat objects."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces import FanInterface, ThermostatInterface

from .port_device import PortDevice


@dataclass(kw_only=True)
class VantageVirtualThermostatPort(PortDevice, ThermostatInterface, FanInterface):
    """Vantage Virtual Thermostat."""

    class Meta:
        name = "Vantage.VirtualThermostat_PORT"

    @dataclass(kw_only=True)
    class Cool:
        cool_stage_1_load: int = field(metadata={"name": "coolStage1Load"})
        cool_stage_1_task: int = field(metadata={"name": "coolStage1Task"})
        cool_stage_2_load: int = field(metadata={"name": "coolStage2Load"})
        cool_stage_2_task: int = field(metadata={"name": "coolStage2Task"})

    @dataclass(kw_only=True)
    class Fan:
        daisy_chain: bool = field(default=True, metadata={"name": "daisyChain"})
        fan_off_when_heat_reached: bool = field(
            default=True, metadata={"name": "fanOffWhenHeatReached"}
        )
        fan_off_when_cool_reached: bool = field(
            default=True, metadata={"name": "fanOffWhenCoolReached"}
        )
        load_high_speed: int = field(metadata={"name": "loadHighSpeed"})
        load_low_speed: int = field(metadata={"name": "loadLowSpeed"})
        load_max_speed: int = field(metadata={"name": "loadMaxSpeed"})
        load_med_speed: int = field(metadata={"name": "loadMedSpeed"})

    @dataclass(kw_only=True)
    class Heat:
        heat_stage_1_load: int = field(metadata={"name": "heatStage1Load"})
        heat_stage_1_task: int = field(metadata={"name": "heatStage1Task"})
        heat_stage_2_load: int = field(metadata={"name": "heatStage2Load"})
        heat_stage_2_task: int = field(metadata={"name": "heatStage2Task"})

    @dataclass(kw_only=True)
    class IndoorSensorHolder:
        indoor_sensor: list[int] = field(
            default_factory=list, metadata={"name": "indoorSensor"}
        )
        indoor_temp_offset: str = field(
            default="0", metadata={"name": "indoorTempOffset"}
        )

    @dataclass(kw_only=True)
    class OutdoorSensorHolder:
        outdoor_sensor: int = field(metadata={"name": "outdoorSensor"})
        outdoor_temp_offset: str = field(
            default="0", metadata={"name": "outdoorTempOffset"}
        )

    change_over_valve: int = field(metadata={"name": "changeOverValve"})
    cool: Cool = field(metadata={"name": "COOL"})
    fan: Fan = field(metadata={"name": "FAN"})
    frost_mail_from: str
    frost_mail_to: str
    heat: Heat = field(metadata={"name": "HEAT"})
    indoor_sensor_holder: IndoorSensorHolder = field(
        metadata={"name": "indoorSensorHolder"}
    )
    outdoor_sensor_holder: OutdoorSensorHolder = field(
        metadata={"name": "outdoorSensorHolder"}
    )
