"""Tests for sending commands and reading replies in CommandClient."""

import pytest

from aiovantage.command_client import CommandClient, CommandResponse
from aiovantage.errors import (
    ClientTimeoutError,
    CommandError,
    FailedError,
    NotInitializedError,
)
from tests.fakes import FakeCommandConnection


def make_client(*lines: str | Exception) -> tuple[CommandClient, FakeCommandConnection]:
    """Build a client whose connection answers with the given inbound lines."""
    client = CommandClient("fake")
    conn = FakeCommandConnection(list(lines))
    client._connection = conn  # type: ignore[assignment]
    return client, conn


async def test_raw_request_skips_interleaved_events() -> None:
    client, conn = make_client(
        "EL: 271 Load.GetLevel 100000",
        "S:LOAD 5 50.000",
        "R:INVOKE 1 75.000 Load.GetLevel",
    )

    assert await client.raw_request("INVOKE 1 Load.GetLevel") == [
        "R:INVOKE 1 75.000 Load.GetLevel"
    ]
    assert conn.written == ["INVOKE 1 Load.GetLevel\n"]


async def test_raw_request_keeps_data_lines() -> None:
    client, _ = make_client("Commands:", "  LOAD", "R:HELP")

    assert await client.raw_request("HELP") == ["Commands:", "  LOAD", "R:HELP"]


@pytest.mark.parametrize(
    ("line", "error"),
    [
        pytest.param("R:ERROR:12 Failed", FailedError, id="failed"),
        pytest.param("R:ERROR:16 Not Initialized", NotInitializedError, id="not-init"),
        pytest.param("R:ERROR:999 Unknown", CommandError, id="unknown-code"),
    ],
)
async def test_raw_request_raises_typed_error(
    line: str, error: type[CommandError]
) -> None:
    client, _ = make_client(line)

    with pytest.raises(error):
        await client.raw_request("INVOKE 1 Load.GetLevel")


async def test_command_parses_response() -> None:
    client, conn = make_client("R:LOAD 1 50.000")

    response = await client.command("LOAD", 1, 50)

    assert conn.written == ["LOAD 1 50\n"]
    assert response == CommandResponse("LOAD", ["1", "50.000"], [])


async def test_raw_request_closes_connection_on_timeout_and_reopens() -> None:
    client, conn = make_client(ClientTimeoutError(), "R:VERSION 4.9.0.2")

    # A timed out read leaves the socket in an unknown state, so it is dropped
    with pytest.raises(ClientTimeoutError):
        await client.raw_request("VERSION")
    assert conn.closed

    # The next request opens a fresh connection instead of reusing the dead one
    assert await client.raw_request("VERSION") == ["R:VERSION 4.9.0.2"]
    assert conn.opens == 2
