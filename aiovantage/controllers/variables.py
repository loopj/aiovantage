from aiovantage.clients.hc import StatusType
from aiovantage.models.variable import Variable
from aiovantage.controllers.base import BaseController


class VariablesController(BaseController[Variable]):
    item_cls = Variable
    vantage_types = ("GMem",)
    status_types = (StatusType.VARIABLE,)
