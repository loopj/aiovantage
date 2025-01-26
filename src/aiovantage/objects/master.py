"""Master (controller) object."""

from dataclasses import dataclass, field

from .system_object import SystemObject


@dataclass
class Master(SystemObject):
    """Master (controller) object."""

    number: int
    volts: float
    amps: float

    # Not available in 2.x firmware
    module_count: int | None = None
    serial_number: int | None = None

    # State
    firmware_version: str | None = field(default=None, metadata={"type": "Ignore"})
    last_updated: int | None = field(default=None, metadata={"type": "Ignore"})
