"""Vantage events."""

from enum import Enum
from typing import Any, Callable, Dict, TypeVar

from typing_extensions import TypeAlias

from .models import SystemObject


class VantageEvent(Enum):
    """Enum with possible Events."""

    OBJECT_ADDED = "add"
    OBJECT_UPDATED = "update"
    OBJECT_DELETED = "delete"


T = TypeVar("T", bound=SystemObject)

EventCallback: TypeAlias = Callable[[VantageEvent, T, Dict[str, Any]], None]
"""Type alias for a Vantage event callback function."""
