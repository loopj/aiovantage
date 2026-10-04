"""Tests for fetching objects from a master in ConfigurationInterface."""

from aiovantage.config_client import ConfigClient, ConfigurationInterface
from aiovantage.objects import Area
from tests.fakes import (
    CLOSE_FILTER_REPLY,
    FakeConfigConnection,
    open_filter_reply,
    results_reply,
)


async def test_get_objects_addresses_the_given_master() -> None:
    client = ConfigClient("fake")
    conn = FakeConfigConnection(
        [
            open_filter_reply(20),
            results_reply(101, 200),
            results_reply(),
            CLOSE_FILTER_REPLY,
        ]
    )
    client._connection = conn  # type: ignore[assignment]

    areas = [
        area
        async for area in ConfigurationInterface.get_objects(
            client, "Area", master=2, as_type=Area
        )
    ]

    assert [area.vid for area in areas] == [101, 200]
    # Every request in the open, fetch, close sequence carries the master
    assert all(req.startswith("<?Master 2?>") for req in conn.written)
    assert len(conn.written) == 4


async def test_get_objects_defaults_to_the_master_at_host() -> None:
    client = ConfigClient("fake")
    conn = FakeConfigConnection(
        [open_filter_reply(10), results_reply(100), results_reply(), CLOSE_FILTER_REPLY]
    )
    client._connection = conn  # type: ignore[assignment]

    areas = [
        area
        async for area in ConfigurationInterface.get_objects(
            client, "Area", as_type=Area
        )
    ]

    assert [area.vid for area in areas] == [100]
    assert not any(req.startswith("<?Master") for req in conn.written)
