"""Tests for the trigger history, system log and module calls in DiagnosticInterface."""

import datetime as dt

from aiovantage.config_client import (
    ConfigClient,
    DiagnosticInterface,
    SysLogType,
    TriggerType,
)
from tests.fakes import FakeConfigConnection


def entry_xml(time_stamp: str, source: int, destination: int, event: int) -> str:
    """Build a trigger history entry, as the controller formats it."""
    return (
        f"<Entry>\n\t<TimeStamp>{time_stamp}</TimeStamp>\n"
        f"\t<Source>{source}</Source>\n\t<Destination>{destination}</Destination>\n"
        f"\t<Event>{event}</Event>\n\t<Param1>1</Param1>\n\t<Param2>0</Param2>\n"
        "</Entry>\n"
    )


def make_client(*replies: str) -> tuple[ConfigClient, FakeConfigConnection]:
    """Build a client whose connection answers with the given replies."""
    client = ConfigClient("fake")
    conn = FakeConfigConnection(list(replies))
    client._connection = conn  # type: ignore[assignment]
    return client, conn


async def test_get_event_log_parses_entries_in_order() -> None:
    client, conn = make_client(
        "<IDiagnostic>\n\t<GetEventLog>\n\t\t<return>"
        + entry_xml("2026-01-02T03:04:05", 100, 200, 1)
        + entry_xml("2026-01-02T03:04:09", 300, 400, 7)
        + "</return>\n\t</GetEventLog>\n</IDiagnostic>\n"
    )

    entries = await DiagnosticInterface.get_event_log(client)

    # The controller only answers when an empty call element is sent
    assert "<GetEventLog><call/>" in conn.written[0]
    assert [(e.source, e.destination) for e in entries] == [(100, 200), (300, 400)]
    assert entries[0].trigger_type is TriggerType.BUTTON_DOWN
    assert entries[1].trigger_type is TriggerType.OUT_OF_RANGE
    assert entries[0].timestamp == dt.datetime(2026, 1, 2, 3, 4, 5)


async def test_get_event_log_when_empty() -> None:
    client, _ = make_client(
        "<IDiagnostic>\n\t<GetEventLog>\n\t\t<return/>\n\t</GetEventLog>\n</IDiagnostic>\n"
    )

    assert await DiagnosticInterface.get_event_log(client) == []


async def test_get_event_log_next_returns_entry_and_none_past_the_end() -> None:
    client, conn = make_client(
        "<IDiagnostic><GetEventLogNext><return><Position>-1</Position>"
        "<TimeStamp>2026-01-02T03:04:05</TimeStamp><Source>100</Source>"
        "<Destination>200</Destination><Event>3</Event><Param1>0</Param1>"
        "<Param2>0</Param2></return></GetEventLogNext></IDiagnostic>\n",
        "<IDiagnostic><GetEventLogNext><return/></GetEventLogNext></IDiagnostic>\n",
    )

    entry = await DiagnosticInterface.get_event_log_next(client, 41)
    past_end = await DiagnosticInterface.get_event_log_next(client, 42)

    assert "<call>41</call>" in conn.written[0]
    assert entry is not None
    assert (entry.position, entry.trigger_type) == (-1, TriggerType.TIMER)
    assert past_end is None


async def test_get_sys_log_parses_entries() -> None:
    client, _ = make_client(
        "<IDiagnostic><GetSysLog><return><Entry><Type>2</Type>"
        "<Time>01-02T03:04:05</Time><Src>Controller</Src>"
        "<Msg>Task 200 Complete: 0</Msg></Entry></return></GetSysLog></IDiagnostic>\n"
    )

    entries = await DiagnosticInterface.get_sys_log(client)

    assert [(e.type, e.time, e.src, e.msg) for e in entries] == [
        (2, "01-02T03:04:05", "Controller", "Task 200 Complete: 0")
    ]
    assert entries[0].log_type is SysLogType.INFORMATION


async def test_get_modules_parses_status_and_errors() -> None:
    client, conn = make_client(
        "<IDiagnostic><GetModules><return><Module><Address>2</Address>"
        "<VID>120</VID><Revision>3</Revision><Type>256</Type>"
        "<Version>1.0.0 (build 1)</Version><Status><Proc0>00</Proc0>"
        "<Proc1>00</Proc1></Status><Errors>5</Errors><Model>SDM12-EM</Model>"
        "</Module></return></GetModules></IDiagnostic>\n"
    )

    modules = await DiagnosticInterface.get_modules(client)

    assert "<call>1</call>" in conn.written[0]
    assert [(m.address, m.vid, m.errors, m.model) for m in modules] == [
        (2, 120, 5, "SDM12-EM")
    ]
    assert modules[0].status is not None
    assert modules[0].status.proc0 == "00"


async def test_get_sys_log_addresses_another_master() -> None:
    client, conn = make_client(
        "<?Master 2?>\n<IDiagnostic><GetSysLog><return/></GetSysLog></IDiagnostic>\n"
    )

    assert await DiagnosticInterface.get_sys_log(client, master=2) == []
    assert conn.written[0].startswith("<?Master 2?><IDiagnostic>")


async def test_event_log_entry_with_unreadable_fields() -> None:
    client, _ = make_client(
        "<IDiagnostic>\n\t<GetEventLog>\n\t\t<return>"
        + entry_xml("not a time", 100, 200, 99)
        + "</return>\n\t</GetEventLog>\n</IDiagnostic>\n"
    )

    [entry] = await DiagnosticInterface.get_event_log(client)

    assert entry.timestamp is None
    assert entry.trigger_type is None
