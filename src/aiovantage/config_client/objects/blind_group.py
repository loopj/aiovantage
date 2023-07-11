"""BlindGroup object."""

from dataclasses import dataclass
from typing import List

from aiovantage.config_client.xml_dataclass import xml_element

from .blind_group_base import BlindGroupBase
from .location_object import LocationObject


@dataclass
class BlindGroup(BlindGroupBase, LocationObject):
    """BlindGroup object."""

    blind_ids: List[int] = xml_element(
        "Blind", wrapper="BlindTable", default_factory=list
    )
