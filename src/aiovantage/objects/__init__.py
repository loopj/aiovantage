"""Vantage objects."""

import datetime as dt
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum, IntEnum


@dataclass
class Parent:
    """Parent type."""

    vid: int
    position: int = field(metadata={"type": "Attribute"})


@dataclass(kw_only=True)
class SystemObject:
    """Base class for all objects."""

    # MTime, DName, not available in 2.x firmware

    vid: int = field(metadata={"name": "VID", "type": "Attribute"})
    master: int = field(metadata={"type": "Attribute"})
    name: str
    model: str
    note: str
    d_name: str | None = None
    m_time: dt.datetime | None = field(
        default=None, metadata={"type": "Attribute", "format": "%Y-%m-%dT%H:%M:%S.%f"}
    )

    @property
    def id(self) -> int:
        """Return the Vantage ID of the object."""
        return self.vid

    @property
    def display_name(self) -> str:
        """Return the display name of the object."""
        return self.d_name or self.name

    @property
    def vantage_type(self) -> str:
        """Return the Vantage type of the object."""
        cls = type(self)
        cls_meta = getattr(cls, "Meta", None)
        return getattr(cls_meta, "name", cls.__qualname__)


@dataclass(kw_only=True)
class BlindBase(SystemObject):
    """Blind base class."""

    shade_orientation: str | None = field(default=None, metadata=dict(type="Attribute"))
    shade_type: str | None = field(default=None, metadata=dict(type="Attribute"))

    # State
    position: Decimal | None = field(default=None, metadata={"type": "Ignore"})


@dataclass
class BlindGroupBase(BlindBase):
    """Blind group base class."""


@dataclass
class Button(SystemObject):
    """Button object."""

    parent: Parent
    down: int
    up: int
    hold: int
    text1: str
    text2: str

    # State
    pressed: bool | None = field(default=None, metadata={"type": "Ignore"})

    @property
    def text(self) -> str:
        """Return the button text."""
        return f"{self.text1}\n{self.text2}" if self.text2 else self.text1


@dataclass
class GMem(SystemObject):
    """GMem (variable) object."""

    @dataclass
    class Tag:
        type: str
        object: bool = field(
            default=False, metadata={"name": "object", "type": "Attribute"}
        )

    @dataclass
    class Data:
        fixed: bool = field(default=False, metadata={"type": "Attribute"})

    data: Data = field(metadata={"name": "data"})
    persistent: bool
    tag: Tag

    # State
    value: int | str | bool | None = field(default=None, metadata={"type": "Ignore"})

    @property
    def is_bool(self) -> bool:
        """Return True if GMem is boolean type."""
        return self.tag.type == "bool"

    @property
    def is_str(self) -> bool:
        """Return True if GMem is string type."""
        return self.tag.type == "Text"

    @property
    def is_int(self) -> bool:
        """Return True if GMem is integer type."""
        return self.tag.type in (
            "Delay",
            "DeviceUnits",
            "Level",
            "Load",
            "Number",
            "Seconds",
            "Task",
            "DegC",
        )

    @property
    def is_object_id(self) -> bool:
        """Return True if GMem is a pointer to an object."""
        return self.tag.object

    @property
    def is_fixed(self) -> bool:
        """Return True if GMem is a fixed point number."""
        return self.data.fixed


@dataclass(kw_only=True)
class LocationObject(SystemObject):
    """Base class for system objects in an area."""

    # Some objects in firmware 2.x do not have Area or Location

    area: int | None = None
    location: str | None = None


@dataclass
class RGBLoadBase(LocationObject):
    """RGB load base class."""

    class ColorType(Enum):
        RGB = "RGB"
        RGBW = "RGBW"
        HSL = "HSL"
        HSIC = "HSIC"
        CCT = "CCT"
        COLOR_CHANNEL = "Color Channel"

    parent: Parent
    color_type: ColorType
    min_temp: int
    max_temp: int

    # State
    hsl: tuple[int, int, int] | None = field(default=None, metadata={"type": "Ignore"})
    rgb: tuple[int, int, int] | None = field(default=None, metadata={"type": "Ignore"})
    rgbw: tuple[int, int, int, int] | None = field(
        default=None, metadata={"type": "Ignore"}
    )
    level: int | None = field(default=None, metadata={"type": "Ignore"})
    color_temp: int | None = field(default=None, metadata={"type": "Ignore"})

    @property
    def is_on(self) -> bool:
        """Return True if the load is on."""
        return bool(self.level)

    @property
    def is_rgb(self) -> bool:
        """Return True if the load is an RGB(W) load."""
        return self.color_type in (
            self.ColorType.RGB,
            self.ColorType.RGBW,
            self.ColorType.HSL,
        )

    @property
    def is_cct(self) -> bool:
        """Return True if the load is a CCT load."""
        return self.color_type == self.ColorType.CCT


@dataclass
class Load(LocationObject):
    """Load object."""

    parent: Parent
    load_type: str
    power_profile: int

    # State
    level: float | None = field(default=None, metadata={"type": "Ignore"})

    @property
    def is_relay(self) -> bool:
        """Return True if the load type is a relay."""
        return self.load_type in (
            "High Voltage Relay",
            "Low Voltage Relay",
            "[MDR8RW101]",
        )

    @property
    def is_motor(self) -> bool:
        """Return True if the load type is a motor."""
        return self.load_type == "Motor"

    @property
    def is_light(self) -> bool:
        """Return True if the load type is inferred to be a light."""
        return not (self.is_relay or self.is_motor)

    @property
    def is_on(self) -> bool:
        """Return True if the load is on."""
        return bool(self.level)


@dataclass
class LoadGroup(LocationObject):
    """LoadGroup object."""

    load_table: list[int] = field(
        default_factory=list, metadata={"name": "Load", "wrapper": "LoadTable"}
    )

    # State
    level: float | None = field(default=None, metadata={"type": "Ignore"})

    @property
    def is_on(self) -> bool:
        """Return True if the load is on."""
        return bool(self.level)


@dataclass
class Master(SystemObject):
    """Master (controller) object."""

    # ModuleCount, SerialNumber, not available in 2.x firmware

    number: int
    volts: float
    amps: float
    module_count: int | None = None
    serial_number: int | None = None

    # State
    firmware_version: str | None = field(default=None, metadata={"type": "Ignore"})
    last_updated: int | None = field(default=None, metadata={"type": "Ignore"})


@dataclass
class Module(SystemObject):
    """Module object."""

    parent: Parent


@dataclass
class ModuleGen2(SystemObject):
    """ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""

    parent: Parent


@dataclass
class PowerProfile(SystemObject):
    """Power Profile object."""

    # Adjust, Freq, Inductive, not available in 2.x firmware

    min: float
    max: float
    adjust: int | None = None
    freq: int | None = None
    inductive: bool | None = None

    @property
    def is_dimmable(self) -> bool:
        """Return True if loads with this profile are dimmable."""
        return self.max > self.min


@dataclass
class DCPowerProfile(PowerProfile):
    """DCPowerProfile object."""


@dataclass
class PWMPowerProfile(DCPowerProfile):
    """PWM power profile object."""


@dataclass
class StationBus(SystemObject):
    """Station bus object."""

    parent: Parent


@dataclass
class Task(SystemObject):
    """Task object."""

    # State
    is_running: bool | None = field(default=None, metadata={"type": "Ignore"})
    state: int | None = field(default=None, metadata={"type": "Ignore"})


@dataclass
class Area(LocationObject):
    """Area object."""


@dataclass
class BackBox(LocationObject):
    """BackBox object."""

    keypad_style: int


@dataclass
class Blind(BlindBase, LocationObject):
    """Blind object."""

    parent: Parent


@dataclass
class BlindGroup(BlindGroupBase, LocationObject):
    """BlindGroup object."""

    blind_table: list[int] = field(
        default_factory=list, metadata={"name": "Blind", "wrapper": "BlindTable"}
    )


@dataclass
class CustomDevice(LocationObject):
    """Base class for custom device objects."""


@dataclass
class ChildDevice(CustomDevice):
    """Base class for child device objects."""

    parent: Parent


@dataclass
class SomfyRS485GroupChild(BlindGroupBase, ChildDevice):
    """Somfy RS-485 SDN 2.0 blind group."""

    class Meta:
        name = "Somfy.RS-485_Group_CHILD"


@dataclass
class SomfyRS485ShadeChild(BlindBase, ChildDevice):
    """Somfy RS-485 SDN 2.0 blind."""

    class Meta:
        name = "Somfy.RS-485_Shade_CHILD"


@dataclass
class SomfyURTSI2GroupChild(BlindGroupBase, ChildDevice):
    """Somfy URTSI 2 blind group."""

    class Meta:
        name = "Somfy.URTSI_2_Group_CHILD"


@dataclass
class SomfyURTSI2ShadeChild(BlindBase, ChildDevice):
    """Somfy URTSI 2 blind."""

    class Meta:
        name = "Somfy.URTSI_2_Shade_CHILD"


@dataclass
class ParentDevice(CustomDevice):
    """Base class for parent device objects."""


@dataclass
class DryContact(LocationObject):
    """DryContact object."""

    parent: Parent

    # State
    triggered: bool | None = field(default=None, metadata={"type": "Ignore"})


@dataclass
class RelayBlind(BlindBase, LocationObject):
    """Relay blind object."""


@dataclass
class StationObject(LocationObject):
    """Base class for all station objects."""

    serial_number: str
    bus: int


@dataclass
class ContactInput(StationObject):
    """Contact Input."""


@dataclass
class DINStation(StationObject):
    """Base class for DIN station objects."""


@dataclass
class DINContactInput(DINStation):
    """DIN Contact Input Station."""


@dataclass
class DINHighVoltageRelayStation(DINStation):
    """DIN High Voltage Relay Station."""


@dataclass
class DINLowVoltageRelayStation(DINStation):
    """DIN Low Voltage Relay Station."""


@dataclass
class EqCtrl(StationObject):
    """Equinox 40 Station."""


@dataclass
class EqUX(StationObject):
    """Equinox 41 or Equinox 73 touchscreen."""


@dataclass
class HighVoltageRelayStation(StationObject):
    """High Voltage Relay Station."""


@dataclass
class Keypad(StationObject):
    """Keypad Station."""

    parent: Parent


@dataclass
class Dimmer(Keypad):
    """ScenePoint Dimmer Station."""


@dataclass
class DualRelayStation(Keypad):
    """ScenePoint Dual Relay Station."""


@dataclass
class ScenePointRelay(Keypad):
    """ScenePoint Relay Station."""


@dataclass
class LowVoltageRelayStation(StationObject):
    """Low Voltage Relay Station."""


@dataclass
class RS232Station(StationObject):
    """RS-232 Station."""


@dataclass
class RS485Station(StationObject):
    """RS-485 Station."""


@dataclass
class QISBlind(BlindBase, StationObject):
    """QIS blind object."""


@dataclass
class QubeBlind(BlindBase, StationObject):
    """Qube blind object."""


@dataclass
class Thermostat(StationObject):
    """Thermostat object."""

    class OperationMode(IntEnum):
        """The operation mode of the thermostat."""

        OFF = 0
        COOL = 1
        HEAT = 2
        AUTO = 3

    class FanMode(IntEnum):
        """The fan mode of the thermostat."""

        AUTO = 0
        ON = 1

    class DayMode(IntEnum):
        """The day mode of the thermostat."""

        DAY = 0
        NIGHT = 1

    class HoldMode(IntEnum):
        """The hold mode of the thermostat."""

        NORMAL = 0
        HOLD = 1

    class Status(IntEnum):
        """The status of the thermostat."""

        OFF = 0
        COOLING = 1
        HEATING = 2
        OFFLINE = 3

    # State
    # "status" Not available in 2.x firmware
    operation_mode: OperationMode | None = field(
        default=None, metadata={"type": "Ignore"}
    )
    fan_mode: FanMode | None = field(default=None, metadata={"type": "Ignore"})
    day_mode: DayMode | None = field(default=None, metadata={"type": "Ignore"})
    hold_mode: HoldMode | None = field(default=None, metadata={"type": "Ignore"})
    status: Status | None = field(default=None, metadata={"type": "Ignore"})


@dataclass
class VantageDmxDaliGateway(StationObject):
    """DMX/DALI Gateway station."""

    class Meta:
        name = "Vantage.DmxDaliGateway"


@dataclass
class Sensor(LocationObject):
    """Sensor object."""


@dataclass
class AnemoSensor(Sensor):
    """AnemoSensor (wind sensor) object."""

    parent: Parent

    # State
    speed: Decimal | None = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )


@dataclass
class LightSensor(Sensor):
    """Light sensor object."""

    parent: Parent

    # State
    level: Decimal | None = field(default=None, metadata={"type": "Ignore"})


@dataclass
class OmniSensor(Sensor):
    """OmniSensor object."""

    class ConversionType(Enum):
        FIXED = "fixed"
        INT = "int"

    @dataclass
    class Get:
        """Omnisensor get method information."""

        @dataclass
        class Formula:
            return_type: "OmniSensor.ConversionType" = field(
                metadata={"type": "Attribute"}
            )
            level_type: "OmniSensor.ConversionType" = field(
                metadata={"type": "Attribute"}
            )
            value: str

        formula: Formula
        method: str
        method_hw: str = field(metadata={"name": "MethodHW"})

    parent: Parent
    get: Get

    # State
    level: int | Decimal | None = field(default=None, metadata={"type": "Ignore"})

    @property
    def is_current_sensor(self) -> bool:
        """Return True if the sensor is a current sensor."""
        return self.model == "Current"

    @property
    def is_power_sensor(self) -> bool:
        """Return True if the sensor is a power sensor."""
        return self.model == "Power"

    @property
    def is_temperature_sensor(self) -> bool:
        """Return True if the sensor is a temperature sensor."""
        return self.model == "Temperature"


@dataclass(kw_only=True)
class Temperature(Sensor):
    """Temperature object."""

    class Setpoint(Enum):
        """Setpoint type."""

        HEAT = "Heat"
        COOL = "Cool"
        AUTO = "Auto"

    # Not available in 2.x firmware
    setpoint: Setpoint | None = field(default=None, metadata={"type": "Attribute"})
    parent: Parent

    # State
    value: Decimal | None = field(default=None, metadata={"type": "Ignore"})


@dataclass
class PortDevice(LocationObject):
    """Base class for Vantage port devices."""

    # NOTE: Inherits from LocationObject on 2.x firmware, ParentDevice on 3.x firmware.


@dataclass
class VantageDDGColorLoad(RGBLoadBase):
    """DMX/DALI Gateway color load object."""

    class Meta:
        name = "Vantage.DDGColorLoad"


@dataclass
class VantageDGColorLoad(RGBLoadBase):
    """DMX Gateway color load object."""

    class Meta:
        name = "Vantage.DGColorLoad"


@dataclass
class VantageDmxGateway(PortDevice):
    """DMX Gateway."""

    class Meta:
        name = "Vantage.DmxGateway"


@dataclass
class SomfyURTSI2Port(PortDevice):
    """Somfy URTSI 2 port device."""

    class Meta:
        name = "Somfy.URTSI_2_PORT"


@dataclass
class SomfyRS485SDN20Port(PortDevice):
    """Somfy RS-485 SDN 2.0."""

    class Meta:
        name = "Somfy.RS-485_SDN_2_x2E_0_PORT"
