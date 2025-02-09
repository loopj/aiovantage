"""Event classes for Vantage controller events."""

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class VantageEvent(Generic[T]):
    """Base class for Vantage controller events."""

    obj: T


@dataclass
class ObjectAddedEvent(VantageEvent[T]):
    """Event emitted when an object is added to the controller."""


@dataclass
class ObjectUpdatedEvent(VantageEvent[T]):
    """Event emitted when an object is updated."""

    attrs_changed: list[str]


@dataclass
class ObjectDeletedEvent(VantageEvent[T]):
    """Event emitted when an object is removed from the controller."""
