from ..clients.hc import StatusType
from ..models.load import Load
from .base import BaseController


class LoadsController(BaseController[Load]):
    item_cls = Load
    vantage_types = ("Load",)
    status_types = (StatusType.LOAD,)