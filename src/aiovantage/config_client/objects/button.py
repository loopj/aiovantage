from dataclasses import dataclass

from aiovantage.config_client.xml_dataclass import xml_element

from .system_object import SystemObject


@dataclass
class Button(SystemObject):
    parent_id: int = xml_element("Parent")
    text1: str = xml_element("Text1")
    text2: str = xml_element("Text2")
