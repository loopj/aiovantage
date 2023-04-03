from aiovantage.clients.hc import StatusType
from aiovantage.controllers.base import BaseController
from aiovantage.models.dry_contact import DryContact


class DryContactsController(BaseController[DryContact]):
    item_cls = DryContact
    vantage_types = ("DryContact",)
    status_types = (StatusType.BTN,)
