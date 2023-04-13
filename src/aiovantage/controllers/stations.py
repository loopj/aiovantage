from aiovantage.aci_client.system_objects import STATION_TYPES, StationObject
from aiovantage.controllers.base import BaseController


class StationsController(BaseController[StationObject]):
    item_cls = StationObject
    vantage_types = tuple(type.__name__ for type in STATION_TYPES)
