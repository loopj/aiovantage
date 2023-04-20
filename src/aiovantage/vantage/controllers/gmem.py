from aiovantage.aci_client.system_objects import GMem
from aiovantage.hc_client import StatusCategory
from aiovantage.vantage.controllers.base import BaseController


class GMemController(BaseController[GMem]):
    item_cls = GMem
    vantage_types = (GMem,)
    status_categories = (StatusCategory.VARIABLE,)
