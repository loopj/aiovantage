from enum import Enum
from typing import Literal, Sequence, TypedDict, Union


class EventType(Enum):
    CONNECTED = "connect"
    DISCONNECTED = "disconnect"
    RECONNECTED = "reconnect"
    STATUS = "status"
    EVENT_LOG = "event_log"


class ConnectEvent(TypedDict):
    tag: Literal[EventType.CONNECTED]


class DisconnectEvent(TypedDict):
    tag: Literal[EventType.DISCONNECTED]


class ReconnectEvent(TypedDict):
    tag: Literal[EventType.RECONNECTED]


class StatusEvent(TypedDict):
    tag: Literal[EventType.STATUS]
    id: int
    status_type: str
    args: Sequence[str]


class EventLogEvent(TypedDict):
    tag: Literal[EventType.EVENT_LOG]
    log: str


Event = Union[ConnectEvent, DisconnectEvent, ReconnectEvent, StatusEvent, EventLogEvent]
