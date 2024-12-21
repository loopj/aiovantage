"""DCPowerProfile object."""

from dataclasses import dataclass

from .power_profile import PowerProfile


@dataclass(kw_only=True)
class DCPowerProfile(PowerProfile):
    """DCPowerProfile object."""

    # NOTE: Inherits from SystemObject on 2.x firmware, PowerProfile on 3.x firmware.
