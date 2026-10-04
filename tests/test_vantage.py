"""Tests for system discovery in the Vantage client."""

from aiovantage import Vantage
from tests.fakes import SYS_INFO_REPLY, FakeConfigConnection


async def test_discover_masters_caches_the_system_shape() -> None:
    vantage = Vantage("fake")
    conn = FakeConfigConnection([SYS_INFO_REPLY])
    vantage.config_client._connection = conn  # type: ignore[assignment]

    await vantage.discover_masters()
    await vantage.discover_masters()

    assert vantage.master_number == 1
    # A peer still in its bootloader cannot answer config requests
    assert vantage.peers == [2]
    # Discovery happens once, later calls return at once
    assert len(conn.written) == 1
