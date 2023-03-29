from ..models.load import Load
from .base import BaseController


class LoadsController(BaseController[Load]):
    item_cls = Load
    vantage_types = ["Load"]
    event_types = ["LOAD"]