"""Interface for querying and controlling variables."""

from dataclasses import dataclass

from .base import Interface, method


class GMemInterface(Interface):
    """Interface for querying and controlling variables."""

    interface_name = "GMem"

    @dataclass
    class Buffer:
        """Response from a GMem fetch operation."""

        rcode: int
        data: bytes
        size: int

    buffer: Buffer | None = None
    value: int | str | bool | None = None  # Not strictly a property

    @method("Fetch", property="buffer")
    async def fetch(self) -> Buffer:
        """Fetch the contents of the variable.

        Returns:
            The contents of the variable.
        """
        # INVOKE <id> GMem.Fetch
        # -> R:INVOKE <id> <rcode> GMem.Fetch <buffer> <size>
        return await self.invoke("GMem.Fetch")

    @method("Commit")
    async def commit(self, buffer: bytes) -> None:
        """Set the contents of the variable.

        Args:
            vid: The Vantage ID of the variable.
            buffer: The contents to set the variable to.
        """
        # INVOKE <id> GMem.Commit <buffer> <size>
        # -> R:INVOKE <id> <rcode> GMem.Commit <buffer> <size>
        await self.invoke("GMem.Commit", buffer)
