from aiovantage.clients.hc import StatusType
from aiovantage.controllers.base import BaseController
from aiovantage.models.variable import Variable


class VariablesController(BaseController[Variable]):
    item_cls = Variable
    vantage_types = ("GMem",)
    status_types = (StatusType.VARIABLE,)
