"""Vantage events."""

from enum import Enum


class VantageEvent(Enum):
    """Enum with possible Events."""

    OBJECT_ADDED = "add"
    OBJECT_UPDATED = "update"
    OBJECT_DELETED = "delete"
