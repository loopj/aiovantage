from ..clients.hc import StatusType
from ..models.dry_contact import DryContact
from .base import BaseController


class DryContactsController(BaseController[DryContact]):
    item_cls = DryContact
    vantage_types = ("DryContact",)
    status_types = (StatusType.BTN,)
