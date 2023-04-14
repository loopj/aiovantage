from dataclasses import dataclass
from typing import Optional

from ..xml_dataclass import xml_element
from .location_object import LocationObject


@dataclass
class Load(LocationObject):
    load_type: Optional[str] = xml_element("LoadType", default=None)

    def __post_init__(self) -> None:
        self.level: Optional[float] = None
