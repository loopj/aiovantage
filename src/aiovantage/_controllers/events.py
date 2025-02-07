from collections.abc import Awaitable, Callable
from enum import Enum
from typing import Any, TypeAlias, TypeVar

from aiovantage.objects import SystemObject


class ControllerEvent(Enum):
    """Event types that can be emitted Vantage controllers or the main client."""

    OBJECT_ADDED = "add"
    """An object was added to the controller."""

    OBJECT_UPDATED = "update"
    """One or more object attributes were updated."""

    OBJECT_DELETED = "delete"
    """An object was removed from the controller."""


T = TypeVar("T", bound=SystemObject)

EventCallback: TypeAlias = Callable[
    [ControllerEvent, T, dict[str, Any]], None | Awaitable[None]
]
"""Type alias for a Vantage event callback function."""
