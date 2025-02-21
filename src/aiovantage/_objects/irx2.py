"""IRX II."""

from dataclasses import dataclass, field

from .station_object import StationObject


@dataclass(kw_only=True)
class IRX2(StationObject):
    """IRX II."""

    @dataclass
    class IRPassThru:
        channel: int = 0
        voltage: bool = False
        power: int = 5
        inverted: bool = False

    ir_pass_thru: IRPassThru = field(metadata={"name": "IRPassThru"})
    led_auto_off: bool = field(default=False, metadata={"name": "LEDAutoOff"})
