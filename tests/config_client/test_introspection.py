"""Tests for parsing system information in IntrospectionInterface."""

import pytest

from aiovantage.config_client import ConfigClient, IntrospectionInterface
from tests.fakes import FakeConfigConnection


def sys_info_reply(peers: str | None) -> str:
    """Build a GetSysInfo reply for master 1 with the given Peers content."""
    peers_xml = "" if peers is None else f"<Peers>{peers}</Peers>"
    return (
        "<IIntrospection><GetSysInfo><return><SysInfo>"
        "<MasterNumber>1</MasterNumber><SerialNumber>5607848</SerialNumber>"
        f"{peers_xml}"
        "</SysInfo></return></GetSysInfo></IIntrospection>\n"
    )


def make_client(*replies: str) -> ConfigClient:
    """Build a client whose connection answers with the given replies."""
    client = ConfigClient("fake")
    client._connection = FakeConfigConnection(list(replies))  # type: ignore[assignment]
    return client


async def test_get_sys_info_parses_master_and_serial() -> None:
    client = make_client(sys_info_reply(""))

    sys_info = await IntrospectionInterface.get_sys_info(client)

    assert sys_info.master_number == 1
    assert sys_info.serial_number == 5607848


@pytest.mark.parametrize(
    ("peers", "app", "boot"),
    [
        pytest.param("", [], [], id="single-master"),
        pytest.param("<App>2</App>", [2], [], id="two-masters"),
        pytest.param("<App>2</App><App>3</App>", [2, 3], [], id="three-masters"),
        pytest.param("<App>2</App><Boot>3</Boot>", [2], [3], id="peer-in-bootloader"),
    ],
)
async def test_get_sys_info_parses_peers(
    peers: str, app: list[int], boot: list[int]
) -> None:
    client = make_client(sys_info_reply(peers))

    sys_info = await IntrospectionInterface.get_sys_info(client)

    assert sys_info.peers is not None
    assert sys_info.peers.app == app
    assert sys_info.peers.boot == boot


async def test_get_sys_info_without_peers_element() -> None:
    # Older firmware may not report peers at all
    client = make_client(sys_info_reply(None))

    sys_info = await IntrospectionInterface.get_sys_info(client)

    assert sys_info.peers is None
