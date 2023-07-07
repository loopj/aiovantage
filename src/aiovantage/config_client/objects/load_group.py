"""LoadGroup object."""

from dataclasses import dataclass
from typing import List, Optional

from aiovantage.config_client.xml_dataclass import xml_element

from .location_object import LocationObject


@dataclass
class LoadGroup(LocationObject):
    """LoadGroup object."""

    load_ids: List[int] = xml_element("Load", wrapper="LoadTable")

    def __post_init__(self) -> None:
        """Declare state attributes in post init."""
        self.level: Optional[float] = None

    @property
    def is_on(self) -> bool:
        """Return True if the load is on."""
        return bool(self.level)
