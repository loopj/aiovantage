from ..models.area import Area
from .base import BaseController


class AreasController(BaseController[Area]):
    item_cls = Area
    vantage_types = ["Area"]
