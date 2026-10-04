"""Tests for populating a controller across masters."""

from aiovantage import Vantage
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
