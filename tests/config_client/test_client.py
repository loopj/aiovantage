"""Tests for addressing and parsing RPC calls in ConfigClient."""

import asyncio

import pytest

from aiovantage.config_client import ConfigClient, ConfigurationInterface
from aiovantage.errors import (
    ClientResponseError,
    ClientTimeoutError,
    LoginRequiredError,
)
from tests.fakes import FakeConfigConnection

OPEN_FILTER_REPLY = """<IConfiguration>
\t<OpenFilter>
\t\t<return>7386048</return>
\t</OpenFilter>
</IConfiguration>
"""


def make_client(
    *replies: str | BaseException,
) -> tuple[ConfigClient, FakeConfigConnection]:
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


async def test_rpc_closes_connection_on_timeout_and_reopens() -> None:
    client, conn = make_client(ClientTimeoutError(), OPEN_FILTER_REPLY)

    # A timed out read leaves its late reply on the socket, so it is dropped
    with pytest.raises(ClientTimeoutError):
        await ConfigurationInterface.open_filter(client, "Load")
    assert conn.closed

    # The next request opens a fresh connection instead of reading the late reply
    assert await ConfigurationInterface.open_filter(client, "Load") == 7386048
    assert conn.opens == 2


async def test_rpc_closes_connection_on_cancel_and_reopens() -> None:
    client, conn = make_client(asyncio.CancelledError(), OPEN_FILTER_REPLY)

    # A canceled read leaves its reply on the socket, so it is dropped
    with pytest.raises(asyncio.CancelledError):
        await ConfigurationInterface.open_filter(client, "Load")
    assert conn.closed

    # The next request opens a fresh connection instead of reading the stale reply
    assert await ConfigurationInterface.open_filter(client, "Load") == 7386048
    assert conn.opens == 2


async def test_rpc_closes_connection_when_setup_fails_and_reopens() -> None:
    client = ConfigClient("fake")
    conn = FakeConfigConnection([OPEN_FILTER_REPLY], open_errors=[ClientTimeoutError()])
    client._connection = conn  # type: ignore[assignment]

    # The setup probe timed out, so its late reply is dropped with the connection
    with pytest.raises(ClientTimeoutError):
        await ConfigurationInterface.open_filter(client, "Load")
    assert conn.closed

    # The next request sets up a fresh connection
    assert await ConfigurationInterface.open_filter(client, "Load") == 7386048
    assert conn.opens == 2


async def test_rpc_queued_behind_a_timeout_uses_a_fresh_connection() -> None:
    client, conn = make_client(ClientTimeoutError(), OPEN_FILTER_REPLY)

    # The second request waits for the first, which times out and closes the socket
    first, second = await asyncio.gather(
        ConfigurationInterface.open_filter(client, "Load"),
        ConfigurationInterface.open_filter(client, "Load"),
        return_exceptions=True,
    )

    assert isinstance(first, ClientTimeoutError)
    assert second == 7386048
    assert conn.opens == 2


async def test_rpc_raises_response_error_on_malformed_reply() -> None:
    client, _ = make_client("<IConfiguration><OpenFilter></IConfiguration>\n")

    with pytest.raises(ClientResponseError):
        await ConfigurationInterface.open_filter(client, "Load")


async def test_rpc_closes_connection_when_login_is_required() -> None:
    client, conn = make_client(OPEN_FILTER_REPLY)
    conn.requires_authentication = True  # type: ignore[misc]

    # LoginRequiredError is a CommandError, and so a ClientError, so setup closes the
    # connection rather than leaving it open for the next request to use unauthenticated
    with pytest.raises(LoginRequiredError):
        await ConfigurationInterface.open_filter(client, "Load")
    assert conn.closed
