from ..clients.hc import StatusType
from ..models.variable import Variable
from .base import BaseController


class VariablesController(BaseController[Variable]):
    item_cls = Variable
    vantage_types = ("GMem",)
    status_types = (StatusType.VARIABLE,)