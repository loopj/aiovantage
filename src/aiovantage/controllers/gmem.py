from aiovantage.aci_client.system_objects import GMem
from aiovantage.controllers.base import BaseController
from aiovantage.hc_client import StatusType


class GMemController(BaseController[GMem]):
    item_cls = GMem
    vantage_types = ("GMem",)
    status_types = (StatusType.VARIABLE,)
