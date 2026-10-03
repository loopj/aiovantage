"""Tests for addressing and parsing RPC calls in ConfigClient."""

from aiovantage.config_client import ConfigClient, ConfigurationInterface
from tests.fakes import FakeConfigConnection

OPEN_FILTER_REPLY = """<IConfiguration>
\t<OpenFilter>
\t\t<return>7386048</return>
\t</OpenFilter>
</IConfiguration>
"""


def make_client(*replies: str) -> tuple[ConfigClient, FakeConfigConnection]:
    """Build a client whose connection answers with the given replies."""
    client = ConfigClient("fake")
    conn = FakeConfigConnection(list(replies))
    client._connection = conn  # type: ignore[assignment]
    return client, conn


async def test_rpc_sends_plain_request_by_default() -> None:
    client, conn = make_client(OPEN_FILTER_REPLY)

    handle = await ConfigurationInterface.open_filter(client, "Load")

    assert handle == 7386048
    assert conn.written[0].startswith("<IConfiguration>")


async def test_rpc_addresses_another_master() -> None:
    client, conn = make_client(OPEN_FILTER_REPLY)

    await ConfigurationInterface.open_filter(client, "Load", master=2)

    assert conn.written[0].startswith("<?Master 2?><IConfiguration>")


async def test_rpc_parses_reply_from_another_master() -> None:
    # A master names itself at the top of its reply, see #369
    client, _ = make_client("<?Master 2?>\n" + OPEN_FILTER_REPLY)

    assert await ConfigurationInterface.open_filter(client, "Load", master=2) == 7386048
