from dataclasses import dataclass

from ..xml_dataclass import xml_element
from .location_object import LocationObject


@dataclass
class DryContact(LocationObject):
    parent_id: int = xml_element("Parent")
