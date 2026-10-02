"""Tests for parsing and routing event stream messages in EventStream."""

from aiovantage.command_client import EventStream
from aiovantage.events import EnhancedLogReceived, StatusReceived


def feed(stream: EventStream, line: str) -> None:
    """Hand one inbound line to the stream as if it was read from the controller."""
    stream._parse_message(line)  # type: ignore[reportPrivateUsage]


def queued(stream: EventStream) -> list[str]:
    """Drain and return the commands queued for sending to the controller."""
    queue = stream._command_queue  # type: ignore[reportPrivateUsage]
    commands: list[str] = []
    while not queue.empty():
        commands.append(queue.get_nowait())
    return commands


async def test_status_line_emits_status_received() -> None:
    stream = EventStream("fake")
    received: list[StatusReceived] = []
    stream.subscribe(StatusReceived, received.append)

    feed(stream, "S:LOAD 5 50.000")

    assert received == [StatusReceived("LOAD", 5, ["50.000"])]


async def test_enhanced_log_line_emits_enhanced_log_received() -> None:
    stream = EventStream("fake")
    received: list[EnhancedLogReceived] = []
    stream.subscribe(EnhancedLogReceived, received.append)

    feed(stream, "EL: 324 Button.GetState 1")

    assert received == [EnhancedLogReceived("324 Button.GetState 1")]


async def test_subscribe_status_filters_by_category() -> None:
    stream = EventStream("fake")
    loads: list[StatusReceived] = []
    everything: list[StatusReceived] = []
    stream.subscribe_status(loads.append, "LOAD")
    stream.subscribe_status(everything.append)

    feed(stream, "S:LOAD 5 50.000")
    feed(stream, "S:TASK 7 1")

    assert [event.category for event in loads] == ["LOAD"]
    assert [event.category for event in everything] == ["LOAD", "TASK"]


async def test_subscribe_status_queues_controller_commands_once() -> None:
    stream = EventStream("fake")

    unsubscribe_first = stream.subscribe_status(lambda _: None, "LOAD")
    unsubscribe_second = stream.subscribe_status(lambda _: None, "LOAD")
    assert queued(stream) == ["STATUS LOAD"]

    unsubscribe_first()
    assert queued(stream) == []

    unsubscribe_second()
    assert queued(stream) == ["STATUS NONE"]
