"""BlindGroup object."""

from dataclasses import dataclass
from typing import List, Optional

from aiovantage.config_client.xml_dataclass import xml_element

from .location_object import LocationObject


@dataclass
class BlindGroup(LocationObject):
    """BlindGroup object."""

    blind_ids: Optional[List[int]] = xml_element(
        "Blind", wrapper="BlindTable", default=None
    )
