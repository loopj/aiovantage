"""Tests for system discovery in the Vantage client."""

from aiovantage import Vantage
from tests.fakes import FakeConfigConnection

SYS_INFO_REPLY = (
    "<IIntrospection><GetSysInfo><return><SysInfo>"
    "<MasterNumber>1</MasterNumber><SerialNumber>5607848</SerialNumber>"
    "<Peers><App>2</App><Boot>3</Boot></Peers>"
    "</SysInfo></return></GetSysInfo></IIntrospection>\n"
)


async def test_discover_masters_addresses_running_peers() -> None:
    vantage = Vantage("fake")
    vantage.config_client._connection = FakeConfigConnection(  # type: ignore[assignment]
        [SYS_INFO_REPLY]
    )

    await vantage.discover_masters()

    # A peer still in its bootloader cannot answer config requests
    assert vantage.other_masters == [2]
