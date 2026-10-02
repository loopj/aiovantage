"""Fakes shared across tests."""


class FakeCommandClient:
    """Stand-in for CommandClient that answers requests from a script.

    Args:
        replies: Maps each request string to the reply lines the controller sends,
            or to an exception to raise in place of a reply.
    """

    def __init__(self, replies: dict[str, list[str] | Exception]) -> None:
        """Initialize the fake with scripted replies."""
        self.replies = replies
        self.sent: list[str] = []

    async def raw_request(self, request: str) -> list[str]:
        """Record the request and return its scripted reply lines."""
        self.sent.append(request)
        reply = self.replies[request]
        if isinstance(reply, Exception):
            raise reply
        return reply


class FakeConnection:
    """Stand-in for CommandConnection that reads lines from a script.

    Args:
        lines: The inbound lines, each returned by one readuntil() call.
    """

    host = "fake"
    port = 3001

    def __init__(self, lines: list[str]) -> None:
        """Initialize the fake with scripted inbound lines."""
        self.lines = list(lines)
        self.written: list[str] = []
        self.closed = True

    async def open(self) -> None:
        """Mark the connection open."""
        self.closed = False

    def close(self) -> None:
        """Mark the connection closed."""
        self.closed = True

    async def authenticate(self, username: str, password: str) -> None:
        """Accept any credentials."""

    async def write(self, message: str) -> None:
        """Record an outbound message."""
        self.written.append(message)

    async def readuntil(self, separator: bytes, timeout: float | None = None) -> str:
        """Return the next scripted line, terminated the way the controller sends it."""
        return self.lines.pop(0) + "\r\n"
