from aiovantage.aci_client.system_objects import POWER_PROFILES, PowerProfile
from aiovantage.vantage.controllers.base import BaseController


class PowerProfilesController(BaseController[PowerProfile]):
    item_cls = PowerProfile
    vantage_types = tuple(type.__name__ for type in POWER_PROFILES)
