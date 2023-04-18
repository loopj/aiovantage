from aiovantage.aci_client.system_objects import (
    STATION_TYPES,
    StationObject,
    xml_tag_from_class,
)
from aiovantage.vantage.controllers.base import BaseController


class StationsController(BaseController[StationObject]):
    item_cls = StationObject
    vantage_types = tuple(xml_tag_from_class(cls) for cls in STATION_TYPES)
