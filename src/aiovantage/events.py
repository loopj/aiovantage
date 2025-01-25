"""Vantage events."""

from collections.abc import Awaitable, Callable
from enum import Enum
from typing import Any, TypeAlias, TypeVar

from .objects import SystemObject


class VantageEvent(Enum):
    """Enum with possible Events."""

    OBJECT_ADDED = "add"
    OBJECT_UPDATED = "update"
    OBJECT_DELETED = "delete"


T = TypeVar("T", bound=SystemObject)

EventCallback: TypeAlias = Callable[
    [VantageEvent, T, dict[str, Any]], None | Awaitable[None]
]
"""Type alias for a Vantage event callback function."""
