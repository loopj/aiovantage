"""Tests for reading replies in BaseConnection."""

import asyncio

import pytest

from aiovantage._command_client.connection import CommandConnection
from aiovantage.errors import ClientConnectionError, ClientResponseError


class FakeWriter:
    """Stand-in for an open StreamWriter."""

    def is_closing(self) -> bool:
        """Report the writer as open."""
        return False

    def close(self) -> None:
        """Accept a close."""


def make_connection(data: bytes, limit: int = 2**16) -> CommandConnection:
    """Build a connection whose socket has already received the given bytes."""
    conn = CommandConnection("fake")
    reader = asyncio.StreamReader(limit=limit)
    reader.feed_data(data)
    conn._reader = reader  # type: ignore[reportPrivateUsage]
    conn._writer = FakeWriter()  # type: ignore[assignment]
    return conn


async def test_readuntil_raises_response_error_on_invalid_utf8() -> None:
    conn = make_connection(b"S:LOAD 5 \xff\r\nS:LOAD 6 0.000\r\n")

    with pytest.raises(ClientResponseError):
        await conn.readuntil(b"\r\n")

    # The unreadable line was consumed, so the next one is read intact
    assert await conn.readuntil(b"\r\n") == "S:LOAD 6 0.000\r\n"


async def test_readuntil_raises_connection_error_when_reply_exceeds_limit() -> None:
    conn = make_connection(b"S:LOAD 5 50.000 and more\r\n", limit=8)

    with pytest.raises(ClientConnectionError):
        await conn.readuntil(b"\r\n")

    # The rest of the reply is still buffered, so the connection is dropped
    assert conn.closed
