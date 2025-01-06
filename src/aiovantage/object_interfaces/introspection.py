"""Interface for controller introspection."""

from enum import IntEnum
from typing import NamedTuple

from .base import Interface, method


class IntrospectionInterface(Interface):
    """Interface for controller introspection."""

    # Types
    class Firmware(IntEnum):
        """Firmware images."""

        Kernel = 0
        RootFs = 1
        Application = 2

    class FirmwareVersion(NamedTuple):
        """A firmware version response."""

        rcode: int
        image: int
        version: str
        size: int

    # Methods
    @method("Introspection.GetFirmwareVersion")
    async def get_firmware_version(self, image: Firmware) -> FirmwareVersion:
        """Get the firmware version.

        Args:
            image: The firmware image to get the version of.
        """
        # INVOKE <id> Introspection.GetFirmwareVersion <image>
        # -> R:INVOKE <id> <rcode> Introspection.GetFirmwareVersion <image> <version>
        return await self.invoke("Introspection.GetFirmwareVersion", image)

    # Additional convenience methods, not part of the Vantage API
    async def get_application_version(self) -> str:
        """Get the application firmware version."""
        response = await self.get_firmware_version(self.Firmware.Application)

        return response.version
