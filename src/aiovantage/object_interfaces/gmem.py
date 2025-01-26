"""Interface for querying and controlling variables."""

from dataclasses import dataclass

from .base import Interface


class GMemInterface(Interface):
    """Interface for querying and controlling variables."""

    @dataclass
    class Buffer:
        """Response from a GMem fetch operation."""

        rcode: int
        data: bytes
        size: int

    method_signatures = {
        "GMem.Fetch": Buffer,
    }

    async def fetch(self, vid: int) -> Buffer:
        """Fetch the contents of the variable.

        Args:
            vid: The Vantage ID of the variable.

        Returns:
            The contents of the variable.
        """
        # INVOKE <id> GMem.Fetch
        # -> R:INVOKE <id> <rcode> GMem.Fetch <buffer> <size>
        return await self.invoke(vid, "GMem.Fetch")

    async def commit(self, vid: int, buffer: bytes) -> None:
        """Set the contents of the variable.

        Args:
            vid: The Vantage ID of the variable.
            buffer: The contents to set the variable to.
        """
        # INVOKE <id> GMem.Commit <buffer> <size>
        # -> R:INVOKE <id> <rcode> GMem.Commit <buffer> <size>
        await self.invoke(vid, "GMem.Commit", buffer)
