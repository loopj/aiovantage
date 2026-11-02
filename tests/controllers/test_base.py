"""Tests for populating a controller across masters."""

from aiovantage import Vantage
from aiovantage.events import EnhancedLogReceived, ObjectUpdated
from aiovantage.objects import Load, Parent
from tests.fakes import (
    CLOSE_FILTER_REPLY,
    SYS_INFO_REPLY,
    FakeConfigConnection,
    open_filter_reply,
    results_reply,
)


async def test_fetch_objects_queries_each_master_and_skips_duplicates() -> None:
    vantage = Vantage("fake")
    conn = FakeConfigConnection(
        [
            SYS_INFO_REPLY,
            # The connected master
            open_filter_reply(10),
            results_reply(100, 101),
            results_reply(),
            CLOSE_FILTER_REPLY,
            # Master 2, which also reports the shared object 101
            open_filter_reply(20),
            results_reply(101, 200),
            results_reply(),
            CLOSE_FILTER_REPLY,
        ]
    )
    vantage.config_client._connection = conn  # type: ignore[assignment]

    await vantage.areas.initialize(fetch_state=False, enable_state_monitoring=False)

    assert sorted(area.vid for area in vantage.areas) == [100, 101, 200]
    # Discovery first, then each master is addressed explicitly in turn
    masters = [req.partition("?>")[0] for req in conn.written[1:]]
    assert masters == ["<?Master 1"] * 4 + ["<?Master 2"] * 4


async def test_enhanced_log_handler_skips_logs_that_are_not_object_status() -> None:
    vantage = Vantage("fake")
    load = Load(
        vid=100,
        master=1,
        name="Load 100",
        model="",
        note="",
        parent=Parent(vid=10, position=1),
        contractor_number="",
        power_profile=0,
    )
    vantage.loads._objects[load.vid] = load  # type: ignore[reportPrivateUsage]
    handler = vantage.loads._handle_enhanced_log_event  # type: ignore[reportPrivateUsage]
    updated: list[ObjectUpdated[Load]] = []
    vantage.loads.subscribe(ObjectUpdated, updated.append)

    # Trigger and system logs share the stream with object status logs, even
    # when they lead with the VID of an object the controller manages
    for log in (
        "100 200 7 0 0",
        "100 Controller Module Offline",
        "100",
        "\u00b2 X.Y 1",
    ):
        handler(EnhancedLogReceived(log))
    assert updated == []

    # Object status logs still reach the object
    handler(EnhancedLogReceived("100 Load.GetLevel 75000"))
    assert [event.attrs_changed for event in updated] == [["level"]]
