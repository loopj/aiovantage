from dataclasses import dataclass
from typing import Optional

from ..xml_dataclass import xml_element
from .location_object import LocationObject


@dataclass
class DryContact(LocationObject):
    parent: Optional[int] = xml_element("Parent", default=None)
