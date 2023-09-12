"""Interface for controller introspection."""

from enum import IntEnum

from .base import Interface
from .parsers import parse_str


class IntrospectionInterface(Interface):
    """Interface for controller introspection."""

    class Firmware(IntEnum):
        """Firmware images."""

        Kernel = 0
        RootFs = 1
        Application = 2

    method_signatures = {
        "Introspection.GetFirmwareVersion": parse_str,
    }

    async def get_firmware_version(self, vid: int, image: Firmware) -> str:
        """Get the firmware version.

        Args:
            vid: The Vantage ID of the controller.
            image: The firmware image to get the version of.
        """
        # INVOKE <id> Introspection.GetFirmwareVersion <image>
        # -> R:INVOKE <id> <rcode> Introspection.GetFirmwareVersion <image> <version>
        return await self.invoke(
            vid, "Introspection.GetFirmwareVersion", image, as_type=str
        )
