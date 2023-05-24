from enum import Enum


class VantageEvent(Enum):
    OBJECT_ADDED = "add"
    OBJECT_UPDATED = "update"
    OBJECT_DELETED = "delete"
