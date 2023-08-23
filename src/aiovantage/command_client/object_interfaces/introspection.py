"""Interface for controller introspection."""

from enum import IntEnum

from .base import Interface

# NOTE: Not available on 2.x firmware


class IntrospectionInterface(Interface):
    """Interface for controller introspection."""

    class Firmware(IntEnum):
        """Firmware images."""

        KERNEL = 0
        ROOT_FS = 1
        APPLICATION = 2

    async def get_firmware_version(self, vid: int, image: Firmware) -> str:
        """Get the firmware version.

        Args:
            vid: The Vantage ID of the controller.
            image: The firmware image to get the version of.
        """
        # INVOKE <id> Introspection.GetFirmwareVersion <image>
        # -> R:INVOKE <id> <rcode> Introspection.GetFirmwareVersion <image> <version>
        response = await self.invoke(vid, "Introspection.GetFirmwareVersion", image)

        return response.args[4].rstrip()
