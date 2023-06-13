from enum import Enum


class VantageEvent(Enum):
    OBJECT_ADDED = "add"
    OBJECT_REMOVED = "remove"
    OBJECT_UPDATED = "update"
