"""Tests for parsing and routing event stream messages in EventStream."""

import asyncio

import pytest

from aiovantage._command_client.events import KEEPALIVE_INTERVAL, READ_TIMEOUT
from aiovantage.command_client import EventStream
from aiovantage.errors import ClientResponseError, ClientTimeoutError
from aiovantage.events import (
    Connected,
    Disconnected,
    EnhancedLogReceived,
    StatusReceived,
)
from tests.fakes import FakeCommandConnection, UnreadableLoginConnection


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


async def test_message_handler_skips_an_unreadable_line() -> None:
    stream = EventStream("fake")
    conn = FakeCommandConnection([ClientResponseError(), "S:LOAD 5 50.000"])
    stream._connection = conn  # type: ignore[assignment]
    events: list[object] = []
    stream.subscribe(StatusReceived, events.append)
    stream.subscribe(Disconnected, events.append)

    task = asyncio.create_task(stream._message_handler())  # type: ignore[reportPrivateUsage]
    await asyncio.sleep(0.05)

    # The line after the unreadable one is still read, on the same connection, and
    # the handler goes on waiting for more
    assert not task.done()
    task.cancel()
    assert [type(event) for event in events] == [StatusReceived]
    assert conn.opens == 1


async def test_message_handler_reconnects_when_login_reply_is_unreadable() -> None:
    stream = EventStream("fake", "user", "pass")
    conn = UnreadableLoginConnection([])
    stream._connection = conn  # type: ignore[assignment]
    events: list[object] = []
    stream.subscribe(Disconnected, events.append)

    task = asyncio.create_task(stream._message_handler())  # type: ignore[reportPrivateUsage]
    await asyncio.sleep(0.05)

    # The handler drops the connection and waits to retry, rather than stopping
    assert not task.done()
    assert conn.closed
    assert [type(event) for event in events] == [Disconnected]
    task.cancel()


async def test_start_closes_connection_when_login_reply_is_unreadable() -> None:
    stream = EventStream("fake", "user", "pass")
    conn = UnreadableLoginConnection([])
    stream._connection = conn  # type: ignore[assignment]

    # The connection is dropped rather than left open with an unknown login result
    with pytest.raises(ClientResponseError):
        await stream.start()
    assert conn.closed


async def test_subscribe_enhanced_log_queues_commands_for_the_master_at_host() -> None:
    stream = EventStream("fake")

    unsubscribe = stream.subscribe_enhanced_log(lambda _: None, "STATUS")
    enabled = queued(stream)
    unsubscribe()

    # Left unnumbered, the commands apply to the connected master
    assert enabled == ["ELAGG ON", "ELENABLE STATUS ON", "ELLOG STATUS ON"]
    # Collecting and writing outlive the session, only the registration is dropped
    assert queued(stream) == ["ELLOG STATUS OFF"]


async def test_subscribe_enhanced_log_enables_writing_on_each_peer() -> None:
    stream = EventStream("fake")

    stream.subscribe_enhanced_log(lambda _: None, "STATUS", peers=[2, 3])

    # The connected master collects first, then every peer writes to it
    assert queued(stream) == [
        "ELAGG ON",
        "ELENABLE STATUS ON",
        "ELLOG STATUS ON",
        "ELENABLE 2 STATUS ON",
        "ELENABLE 3 STATUS ON",
    ]


async def test_subscribe_enhanced_log_queues_each_command_once() -> None:
    stream = EventStream("fake")

    stream.subscribe_enhanced_log(lambda _: None, "STATUS", peers=[2])
    queued(stream)
    stream.subscribe_enhanced_log(lambda _: None, "STATUS", "STATUSEX", peers=[2])

    # Only the log type the second subscriber added is new
    assert queued(stream) == [
        "ELAGG ON",
        "ELENABLE STATUSEX ON",
        "ELLOG STATUSEX ON",
        "ELENABLE 2 STATUSEX ON",
    ]
