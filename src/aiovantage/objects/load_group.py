"""LoadGroup object."""

from dataclasses import dataclass, field

from .location_object import LocationObject


@dataclass
class LoadGroup(LocationObject):
    """LoadGroup object."""

    load_table: list[int] = field(
        default_factory=list,
        metadata={
            "name": "Load",
            "wrapper": "LoadTable",
        },
    )

    level: float | None = field(
        default=None,
        metadata={
            "type": "Ignore",
        },
    )

    @property
    def is_on(self) -> bool:
        """Return True if the load is on."""
        return bool(self.level)
