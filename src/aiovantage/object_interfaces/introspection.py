"""Interface for controller introspection."""

from enum import IntEnum
from typing import NamedTuple

from .base import Interface


class IntrospectionInterface(Interface):
    """Interface for controller introspection."""

    class Firmware(IntEnum):
        """Firmware images."""

        Kernel = 0
        RootFs = 1
        Application = 2

    class GetFirmwareVersionResponse(NamedTuple):
        """A firmware version response."""

        rcode: int
        image: int
        version: str
        size: int

    method_signatures = {
        "Introspection.GetFirmwareVersion": GetFirmwareVersionResponse,
    }

    # Methods
    async def get_firmware_version(self, image: Firmware) -> str:
        """Get the firmware version.

        Args:
            image: The firmware image to get the version of.
        """
        # INVOKE <id> Introspection.GetFirmwareVersion <image>
        # -> R:INVOKE <id> <rcode> Introspection.GetFirmwareVersion <image> <version>
        response = await IntrospectionInterface.invoke(
            self,
            "Introspection.GetFirmwareVersion",
            image,
            as_type=self.GetFirmwareVersionResponse,
        )

        return response.version
