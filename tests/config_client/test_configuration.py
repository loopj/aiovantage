"""Tests for fetching objects across masters in ConfigurationInterface."""

from aiovantage.config_client import ConfigClient, ConfigurationInterface
from aiovantage.objects import Area
from tests.fakes import FakeConfigConnection


def open_filter_reply(handle: int) -> str:
    """Build an OpenFilter reply for the given handle."""
    return f"<IConfiguration><OpenFilter><return>{handle}</return></OpenFilter></IConfiguration>\n"


def results_reply(*vids: int) -> str:
    """Build a GetFilterResults reply holding one Area per vid, or an empty page."""
    objects = "".join(
        f'<Object VID="{vid}"><Area VID="{vid}" Master="1"><Name>Area {vid}</Name>'
        f"<Model/><Note/><AreaType>Room</AreaType></Area></Object>"
        for vid in vids
    )
    return (
        "<IConfiguration><GetFilterResults><return>"
        f"{objects}"
        "</return></GetFilterResults></IConfiguration>\n"
    )


CLOSE_FILTER_REPLY = "<IConfiguration><CloseFilter><return>true</return></CloseFilter></IConfiguration>\n"


async def test_get_objects_queries_each_master_and_skips_duplicates() -> None:
    client = ConfigClient("fake")
    conn = FakeConfigConnection(
        [
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
    client._connection = conn  # type: ignore[assignment]

    areas = [
        area
        async for area in ConfigurationInterface.get_objects(
            client, "Area", masters=[2], as_type=Area
        )
    ]

    assert [area.vid for area in areas] == [100, 101, 200]
    assert [req.startswith("<?Master 2?>") for req in conn.written] == [False] * 4 + [
        True
    ] * 4


async def test_get_objects_queries_only_the_connected_master_by_default() -> None:
    client = ConfigClient("fake")
    conn = FakeConfigConnection(
        [open_filter_reply(10), results_reply(100), results_reply(), CLOSE_FILTER_REPLY]
    )
    client._connection = conn  # type: ignore[assignment]

    areas = [area async for area in ConfigurationInterface.get_objects(client, "Area")]

    assert len(areas) == 1
    assert len(conn.written) == 4
    assert not any(req.startswith("<?Master") for req in conn.written)
