"""Master (controller) object."""

from dataclasses import dataclass, field
from typing import Optional

from .system_object import SystemObject


@dataclass
class Master(SystemObject):
    """Master (controller) object."""

    number: int = field(
        metadata={
            "name": "Number",
        }
    )

    volts: float = field(
        metadata={
            "name": "Volts",
        }
    )

    amps: float = field(
        metadata={
            "name": "Amps",
        }
    )

    module_count: int = field(
        metadata={
            "name": "ModuleCount",
        }
    )

    serial_number: int = field(
        metadata={
            "name": "SerialNumber",
        }
    )

    firmware_version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

    last_updated: Optional[int] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )
