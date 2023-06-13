from dataclasses import dataclass
from typing import List

from aiovantage.config_client.xml_dataclass import xml_element

from .location_object import LocationObject


@dataclass
class LoadGroup(LocationObject):
    load_ids: List[int] = xml_element("Load", metadata={"wrapper": "LoadTable"})