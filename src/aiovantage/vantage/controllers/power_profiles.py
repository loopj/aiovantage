from aiovantage.aci_client.system_objects import (
    PowerProfile,
    DCPowerProfile,
    PWMPowerProfile,
)
from aiovantage.vantage.controllers.base import BaseController


class PowerProfilesController(BaseController[PowerProfile]):
    item_cls = PowerProfile
    vantage_types = (PowerProfile, DCPowerProfile, PWMPowerProfile)
