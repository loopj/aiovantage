from enum import Enum


class VantageEvent(Enum):
    """Enum with possible Events."""

    OBJECT_ADDED = "add"
    OBJECT_REMOVED = "remove"
    OBJECT_UPDATED = "update"
