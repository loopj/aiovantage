"""Tests for parsing and routing event stream messages in EventStream."""

import asyncio

from aiovantage._command_client.events import KEEPALIVE_INTERVAL, READ_TIMEOUT
from aiovantage.command_client import EventStream
from aiovantage.config_client import SysLogType, TriggerType
from aiovantage.errors import ClientTimeoutError
from aiovantage.events import (
    Connected,
    Disconnected,
    EnhancedLogReceived,
    StatusReceived,
    SystemLogReceived,
    TriggerReceived,
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


async def test_subscribe_triggers_enables_the_event_log() -> None:
    stream = EventStream("fake")

    stream.subscribe_triggers(lambda _: None, peers=[2])

    assert queued(stream) == [
        "ELAGG ON",
        "ELENABLE EVENT ON",
        "ELLOG EVENT ON",
        "ELENABLE 2 EVENT ON",
    ]


async def test_subscribe_triggers_parses_trigger_logs_only() -> None:
    stream = EventStream("fake")
    received: list[TriggerReceived] = []
    stream.subscribe_triggers(received.append)

    # Trigger, object status and system logs all arrive as "EL:" lines
    feed(stream, "EL: 100 200 7 0 0")
    feed(stream, "EL: 324 Button.GetState 1")
    feed(stream, "EL: 2 Controller Accepted config connection from 'host'")

    assert received == [TriggerReceived(100, 200, 7, 0, 0)]


async def test_subscribe_system_log_parses_system_logs_only() -> None:
    stream = EventStream("fake")
    received: list[SystemLogReceived] = []
    stream.subscribe_system_log(received.append)
    assert queued(stream) == ["ELAGG ON", "ELENABLE SYSTEM ON", "ELLOG SYSTEM ON"]

    feed(stream, "EL: 3 Controller [ALERT] Module 'Module 9' (VID:120) lost a feed ")
    feed(stream, "EL: 2 Controller Module Offline: 1.9 [120] ")
    feed(stream, "EL: 100 200 7 0 0")
    feed(stream, "EL: 324 Button.GetState 1")

    assert received == [
        SystemLogReceived(
            3, "Controller", "[ALERT] Module 'Module 9' (VID:120) lost a feed"
        ),
        SystemLogReceived(2, "Controller", "Module Offline: 1.9 [120]"),
    ]


async def test_trigger_parse_keeps_codes_outside_the_known_types() -> None:
    # A module alert, observed when a module lost its first line feed
    assert TriggerReceived.parse("120 300 40964 1 0") == TriggerReceived(
        120, 300, 0xA004, 1, 0
    )


async def test_log_shapes_parse_as_exactly_one_kind() -> None:
    # Enhanced logs carry no type tag, so each shape must match only one parser
    assert SystemLogReceived.parse("100 -1 7 0 0") is None
    assert TriggerReceived.parse("100 -1 7 0 0") == TriggerReceived(100, -1, 7, 0, 0)
    assert TriggerReceived.parse("2 Controller Module Online: 1.9 [120]") is None
    assert SystemLogReceived.parse("324 Button.GetState 1") is None
    assert TriggerReceived.parse("324 Button.GetState 1") is None


async def test_system_log_parse_tolerates_extra_whitespace() -> None:
    parsed = SystemLogReceived.parse("3  Controller	[ALERT] lost a feed ")

    assert parsed == SystemLogReceived(3, "Controller", "[ALERT] lost a feed")
    assert parsed is not None
    assert parsed.log_type is SysLogType.WARNING


async def test_system_log_parse_rejects_a_log_with_no_message() -> None:
    assert SystemLogReceived.parse("3 Controller") is None
    assert SystemLogReceived.parse("3 Controller   ") is None
    assert SystemLogReceived.parse("3") is None


async def test_trigger_type_property_names_known_codes_only() -> None:
    assert TriggerReceived(100, 200, 0, 1, 0).trigger_type is TriggerType.BUTTON_UP
    assert TriggerReceived(120, 300, 0xA004, 1, 0).trigger_type is (
        TriggerType.MODULE_ALERT
    )
    assert TriggerReceived(100, 200, 99, 0, 0).trigger_type is None


async def test_unsubscribe_triggers_stops_the_event_log_once_unused() -> None:
    stream = EventStream("fake")
    received: list[TriggerReceived] = []
    unsubscribe = stream.subscribe_triggers(received.append)
    unsubscribe_other = stream.subscribe_triggers(lambda _: None)
    queued(stream)

    # The log stays on while another subscriber still wants it
    unsubscribe()
    assert queued(stream) == []
    feed(stream, "EL: 100 200 7 0 0")
    assert received == []

    unsubscribe_other()
    assert queued(stream) == ["ELLOG EVENT OFF"]
