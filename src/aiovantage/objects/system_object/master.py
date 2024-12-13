"""Master (controller) object."""

from dataclasses import dataclass

from aiovantage.object_interfaces.introspection import IntrospectionInterface

from . import SystemObject


@dataclass(kw_only=True)
class Master(SystemObject, IntrospectionInterface):
    """Master (controller) object."""

    # NOTE: module_count, serial_number are not available in 2.x firmware

    number: int
    volts: float
    amps: float
    module_count: int | None = None
    serial_number: int | None = None
