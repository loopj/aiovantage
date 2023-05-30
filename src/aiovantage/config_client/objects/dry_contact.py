from dataclasses import dataclass
from enum import Enum

from aiovantage.config_client.xml_dataclass import xml_element

from .location_object import LocationObject


@dataclass
class DryContact(LocationObject):
    class State(Enum):
        UP = 0
        DOWN = 1

    parent_id: int = xml_element("Parent")

    def __post_init__(self) -> None:
        self.state: DryContact.State = DryContact.State.UP