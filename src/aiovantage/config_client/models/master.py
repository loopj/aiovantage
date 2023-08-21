"""Master (controller) object."""

from typing import Optional

from attr import define, field

from .system_object import SystemObject


@define
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

    # Not available in 2.x firmware
    module_count: Optional[int] = field(
        metadata={
            "name": "ModuleCount",
        }
    )

    # Not available in 2.x firmware
    serial_number: Optional[int] = field(
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
