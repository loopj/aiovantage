from aiovantage.aci_client.system_objects import GMem
from aiovantage.vantage.controllers.base import BaseController


class GMemController(BaseController[GMem]):
    item_cls = GMem
    vantage_types = (GMem,)
    status_types = ("VARIABLE",)
