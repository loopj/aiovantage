"""Interface for querying and controlling variables."""

from dataclasses import dataclass

from .base import Interface, method

STRING_HEADER = b"\x01\x00\x00\x00\x20\x00\x00\x00"


class GMemInterface(Interface):
    """Interface for querying and controlling variables."""

    @dataclass
    class Buffer:
        """Response from a GMem fetch operation."""

        @property
        def value(self) -> int | str:
            """Return the value of the variable."""
            # Decode an integer buffer
            if self.rcode == 1:
                # Make sure the buffer is a multiple of 4 bytes
                if not len(self.data) % 4 == 0:
                    raise ValueError("Invalid integer buffer")

                # Integer buffers are signed, little-endian, 32-bit integers
                return int.from_bytes(self.data, "little", signed=True)

            # Decode a string buffer
            if self.rcode == 34:
                # Make sure the buffer has the correct header
                if self.data[:8] != STRING_HEADER:
                    raise ValueError("Invalid string buffer")

                # String buffers have an 8-byte header and are null-terminated
                return self.data[8:].split(b"\x00")[0].decode("ascii")

            raise ValueError(f"Unknown GMem data type: {self.rcode}")

        rcode: int
        data: bytes
        size: int

    # Properties
    buffer: Buffer | None = None

    # Methods
    @method("GMem.Fetch", property="buffer")
    async def fetch(self) -> Buffer:
        """Fetch the contents of the variable."""
        # INVOKE <id> GMem.Fetch
        # -> R:INVOKE <id> <rcode> GMem.Fetch <buffer> <size>
        return await self.invoke("GMem.Fetch")

    @method("GMem.Commit")
    async def commit(self, buffer: bytes) -> None:
        """Set the contents of the variable."""
        # INVOKE <id> GMem.Commit <buffer> <size>
        # -> R:INVOKE <id> <rcode> GMem.Commit <buffer> <size>
        await self.invoke("GMem.Commit", buffer)

    # Convenience functions, not part of the interface
    async def set_value(self, value: int | str) -> None:
        """Set the value of the variable."""
        # NOTE: The `GMem.Commit` method is marked as "INTERNAL", so although it seems
        # to work fine when encoding values to bytes and sending them via GMem.Commit,
        # we're falling back to using `VARIABLE` commands directly, to be nice.

        # Make sure we have a vid to invoke the method on
        if (vid := getattr(self, "vid", None)) is None:
            raise ValueError("The object must have a vid attribute to invoke methods.")

        # Make sure we have a command client to send requests with
        if self.command_client is None:
            raise ValueError("The object has no command client to send requests with.")

        await self.command_client.command("VARIABLE", vid, value, force_quotes=True)

    async def get_value(self) -> int | str:
        """Get the value of the variable."""
        response = await self.fetch()
        return response.value
