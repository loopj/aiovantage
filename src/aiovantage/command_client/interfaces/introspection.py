from enum import Enum

from .base import Interface


class IntrospectionInterface(Interface):
    class Firmware(Enum):
        KERNEL = 0
        ROOT_FS = 1
        APPLICATION = 2

    async def get_firmware_version(self, id: int, image: Firmware) -> str:
        """
        Get the firmware version.

        Args:
            id: The ID of the object.
            firmware: The firmware to get the version of.
        """

        # INVOKE <id> IntroSpection.GetFirmwareVersion <image>
        # -> R:INVOKE <id> <rcode> IntroSpection.GetFirmwareVersion <image> <version>
        response = await self.invoke(
            id, "IntroSpection.GetFirmwareVersion", image.value
        )

        return response.args[4].rstrip()
