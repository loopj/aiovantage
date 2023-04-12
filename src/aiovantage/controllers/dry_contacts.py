from aiovantage.aci_client.system_objects import DryContact
from aiovantage.controllers.base import BaseController
from aiovantage.hc_client import StatusType


class DryContactsController(BaseController[DryContact]):
    item_cls = DryContact
    vantage_types = ("DryContact",)
    status_types = (StatusType.BTN,)
