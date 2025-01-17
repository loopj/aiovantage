"""Interface for querying and controlling variables."""

from dataclasses import dataclass

from .base import Interface, method

STRING_HEADER = b"\x01\x00\x00\x00\x20\x00\x00\x00"


def encode_string_buffer(string: str) -> bytes:
    """Create a string buffer."""
    return STRING_HEADER + string.encode("ascii") + b"\x00"


def decode_string_buffer(buffer: bytes) -> str:
    """Decode a string buffer."""
    if buffer[:8] != STRING_HEADER:
        raise ValueError("Invalid string buffer")

    # Remove the header and split at the null terminator
    return buffer[8:].split(b"\x00")[0].decode("ascii")


def encode_int_buffer(value: int) -> bytes:
    """Create an integer buffer."""
    return value.to_bytes(4, "little", signed=True)


def decode_int_buffer(buffer: bytes) -> int:
    """Decode an integer buffer."""
    if not len(buffer) % 4 == 0:
        raise ValueError("Invalid integer buffer")

    return int.from_bytes(buffer, "little", signed=True)


class GMemInterface(Interface):
    """Interface for querying and controlling variables."""

    @dataclass
    class Buffer:
        """Response from a GMem fetch operation."""

        @property
        def value(self) -> int | str:
            """Return the value of the variable."""
            if self.rcode == 1:
                return decode_int_buffer(self.data)

            if self.rcode == 34:
                return decode_string_buffer(self.data)

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
        if isinstance(value, int):
            buffer = encode_int_buffer(value)
        else:
            buffer = encode_string_buffer(value)

        await self.commit(buffer)

    async def get_value(self) -> int | str:
        """Get the value of the variable."""
        response = await self.fetch()
        return response.value
