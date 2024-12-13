"""DCPowerProfile object."""

from dataclasses import dataclass

from .. import PowerProfile


@dataclass
class DCPowerProfile(PowerProfile):
    """DCPowerProfile object."""

    # NOTE: Inherits from SystemObject on 2.x firmware
