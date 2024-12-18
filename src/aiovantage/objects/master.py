"""Master (controller) object."""

from dataclasses import dataclass, field

from .system_object import SystemObject


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
