"""Master (InFusion Controller) object."""

from dataclasses import dataclass

from aiovantage.object_interfaces import ConfigurationInterface, IntrospectionInterface

from .system_object import SystemObject


@dataclass(kw_only=True)
class Master(SystemObject, IntrospectionInterface, ConfigurationInterface):
    """Master (InFusion Controller) object."""

    number: int
    boot: int = 0
    volts: float
    amps: float
    module_count: int | None = None
    serial_number: int | None = None
