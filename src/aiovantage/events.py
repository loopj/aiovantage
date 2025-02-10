"""Event classes for Vantage controller events."""

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

T = TypeVar("T")

__all__ = [
    "Connected",
    "Disconnected",
    "Reconnected",
    "StatusReceived",
    "EnhancedLogReceived",
    "ObjectAdded",
    "ObjectUpdated",
    "ObjectDeleted",
]


class EventDispatcher:
    """Simple event dispatcher that allows subscription to and emission of events."""

    def __init__(self) -> None:
        """Initialize the event dispatcher."""
        self._subscribers: dict[type, list[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(
        self, event_type: type[T], callback: Callable[[T], None]
    ) -> Callable[[], None]:
        """Register a callback function to be called when an event is emitted.

        Args:
            event_type: Event type to subscribe to.
            callback: Callback function to call when an event of this type is emitted.

        Returns:
            A function that can be called to unsubscribe from the event.
        """
        self._subscribers[event_type].append(callback)

        def unsubscribe() -> None:
            self._subscribers[event_type].remove(callback)
            if not self._subscribers[event_type]:
                del self._subscribers[event_type]

        return unsubscribe

    def emit(self, event: Any) -> None:
        """Emit an event, notifying all subscribers.

        Args:
            event: The event to emit.
        """
        event_type = type(event)  # type: ignore
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(event)


class Connected:
    """Event emitted when a client connection is established."""


class Disconnected:
    """Event emitted when the client connection is lost."""


class Reconnected:
    """Event emitted when the client connection is re-established."""


@dataclass
class StatusReceived:
    """Event emitted when a "S:" status is received."""

    category: str
    """The status category, eg. "LOAD", "BLIND", etc."""

    vid: int
    """The unique Vantage ID of the object the status applies to."""

    args: list[str]
    """The arguments of the status message."""


@dataclass
class EnhancedLogReceived:
    """Event emitted when an "EL:" enhanced log is received."""

    log: str
    """The enhanced log message."""


@dataclass
class ObjectAdded(Generic[T]):
    """Event emitted when an object is added to a controller."""

    obj: T
    """The object that the event is related to."""


@dataclass
class ObjectUpdated(Generic[T]):
    """Event emitted when an object is updated."""

    obj: T
    """The object that the event is related to."""

    attrs_changed: list[str]
    """A list of attributes that have changed."""


@dataclass
class ObjectDeleted(Generic[T]):
    """Event emitted when an object is removed from a controller."""

    obj: T
    """The object that the event is related to."""
