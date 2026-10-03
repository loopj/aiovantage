"""Tests for parsing and routing event stream messages in EventStream."""

import asyncio

from aiovantage._command_client.events import KEEPALIVE_INTERVAL, READ_TIMEOUT
from aiovantage.command_client import EventStream
from aiovantage.errors import ClientTimeoutError
from aiovantage.events import (
    Connected,
    Disconnected,
    EnhancedLogReceived,
    StatusReceived,
)
from tests.fakes import FakeCommandConnection


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


async def test_message_handler_reads_with_a_timeout_and_drops_a_dead_link() -> None:
    stream = EventStream("fake")
    conn = FakeCommandConnection(["S:LOAD 5 50.000", ClientTimeoutError()])
    stream._connection = conn  # type: ignore[assignment]
    events: list[object] = []
    stream.subscribe(Connected, events.append)
    stream.subscribe(Disconnected, events.append)

    task = asyncio.create_task(stream._message_handler())  # type: ignore[reportPrivateUsage]
    await asyncio.sleep(0.05)
    task.cancel()

    # Silence on the link for longer than the keepalive interval means it is dead
    assert conn.timeouts == [READ_TIMEOUT, READ_TIMEOUT]
    assert READ_TIMEOUT > KEEPALIVE_INTERVAL
    # The socket is closed so the retry opens a fresh one rather than flapping
    assert conn.closed
    assert [type(event) for event in events] == [Connected, Disconnected]


async def test_subscribe_enhanced_log_queues_commands_for_the_connected_master() -> (
    None
):
    stream = EventStream("fake")

    stream.subscribe_enhanced_log(lambda _: None, "STATUS")

    # Left unnumbered, the commands apply to the master we are connected to
    assert queued(stream) == ["ELAGG ON", "ELENABLE STATUS ON", "ELLOG STATUS ON"]


async def test_subscribe_enhanced_log_enables_logging_on_every_master() -> None:
    stream = EventStream("fake")
    stream._connection = FakeCommandConnection([])  # type: ignore[assignment]
    await stream.start(other_masters=[2, 3])

    unsubscribe = stream.subscribe_enhanced_log(lambda _: None, "STATUS")
    enabled = queued(stream)
    unsubscribe()
    stream.stop()

    # Only the connected master collects the log, but every master writes to it
    assert enabled == [
        "ELAGG ON",
        "ELENABLE STATUS ON",
        "ELENABLE 2 STATUS ON",
        "ELENABLE 3 STATUS ON",
        "ELLOG STATUS ON",
    ]
    assert queued(stream) == [
        "ELENABLE STATUS OFF",
        "ELENABLE 2 STATUS OFF",
        "ELENABLE 3 STATUS OFF",
        "ELLOG STATUS OFF",
    ]
