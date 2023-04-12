from dataclasses import dataclass
from typing import Optional

from ..xml_dataclass import xml_element
from .system_object import SystemObject


@dataclass
class Button(SystemObject):
    parent: Optional[int] = xml_element("Parent", default=None)
    text1: Optional[str] = xml_element("Text1", default=None)
    text2: Optional[str] = xml_element("Text2", default=None)
