"""Master (controller) object."""

from dataclasses import dataclass, field

from aiovantage.object_interfaces import ConfigurationInterface, IntrospectionInterface

from .system_object import SystemObject


@dataclass(kw_only=True)
class Master(SystemObject, IntrospectionInterface, ConfigurationInterface):
    """Master (InFusion Controller) object."""

    @dataclass
    class DINEnclosure:
        enclosure: int
        position: int = field(metadata={"type": "Attribute"})
        row: int = field(metadata={"type": "Attribute"})

    number: int
    boot: int = 0
    volts: float = 24.0
    amps: float = 2.5

    # Not available in 2.x firmware
    din_enclosure: DINEnclosure | None = field(
        default=None,
        metadata={
            "name": "DINEnclosure",
        },
    )
    module_count: int | None = None
    power_supply: int | None = None
    serial_number: int | None = None
