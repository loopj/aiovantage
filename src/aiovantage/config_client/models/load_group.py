"""LoadGroup object."""

from typing import List, Optional

from attr import define, field

from .location_object import LocationObject


@define
class LoadGroup(LocationObject):
    """LoadGroup object."""

    load_ids: List[int] = field(
        # default_factory=list,
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
