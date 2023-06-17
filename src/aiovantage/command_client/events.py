"""Command client events."""

from enum import Enum
from typing import Literal, Sequence, TypedDict, Union


class EventType(Enum):
    """Enumeration of event types."""

    CONNECTED = "connect"
    DISCONNECTED = "disconnect"
    RECONNECTED = "reconnect"
    STATUS = "status"
    EVENT_LOG = "event_log"


class ConnectEvent(TypedDict):
    """Client connected to the Host Command service."""

    tag: Literal[EventType.CONNECTED]


class DisconnectEvent(TypedDict):
    """Client disconnected from the Host Command service."""

    tag: Literal[EventType.DISCONNECTED]


class ReconnectEvent(TypedDict):
    """Client reconnected to the Host Command service."""

    tag: Literal[EventType.RECONNECTED]


class StatusEvent(TypedDict):
    """Status message received from the Host Command service."""

    tag: Literal[EventType.STATUS]
    id: int
    status_type: str
    args: Sequence[str]


class EventLogEvent(TypedDict):
    """Event log message received from the Host Command service."""

    tag: Literal[EventType.EVENT_LOG]
    log: str


Event = Union[ConnectEvent, DisconnectEvent, ReconnectEvent, StatusEvent, EventLogEvent]
