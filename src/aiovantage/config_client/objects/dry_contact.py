from dataclasses import dataclass

from aiovantage.config_client.xml_dataclass import xml_element

from .location_object import LocationObject


@dataclass
class DryContact(LocationObject):
    parent_id: int = xml_element("Parent")

    def __post_init__(self) -> None:
        self.triggered: bool = False
