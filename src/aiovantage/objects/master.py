"""Master (InFusion Controller) object."""

from dataclasses import dataclass

from aiovantage.object_interfaces import ConfigurationInterface, IntrospectionInterface

from .system_object import SystemObject


@dataclass(kw_only=True)
class Master(SystemObject, IntrospectionInterface, ConfigurationInterface):
    """Master (InFusion Controller) object."""

    # ModuleCount, SerialNumber, not available in 2.x firmware

    number: int
    volts: float
    amps: float
    module_count: int | None = None
    serial_number: int | None = None
