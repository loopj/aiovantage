"""LoadGroup object."""

from dataclasses import dataclass, field
from typing import List, Optional

from .location_object import LocationObject


@dataclass
class LoadGroup(LocationObject):
    """LoadGroup object."""

    load_ids: List[int] = field(
        metadata={
            "name": "Load",
            "wrapper": "LoadTable",
        },
    )

    level: Optional[float] = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

    @property
    def is_on(self) -> bool:
        """Return True if the load is on."""
        return bool(self.level)
