"""Interface for controller introspection."""

from dataclasses import dataclass
from enum import IntEnum

from .base import Interface, method


class IntrospectionInterface(Interface):
    """Interface for controller introspection."""

    # Types
    class Firmware(IntEnum):
        """Firmware image."""

        KERNEL = 0
        ROOT_FS = 1
        APPLICATION = 2

    class LicenseType(IntEnum):
        """License type."""

        UNKNOWN = 0
        EQUINOX = 1
        ALL = -1

    @dataclass
    class FirmwareVersion:
        """A firmware version response."""

        rcode: int
        image: "IntrospectionInterface.Firmware"
        version: str
        size: int

    @dataclass
    class LicenseInfo:
        """A license info response."""

        rcode: int
        type: "IntrospectionInterface.LicenseType"
        used: int
        total: int

    # Methods
    @method("Introspection.GetAppControllers")
    async def get_app_controllers(self) -> str:
        """Get a list of controllers in application mode, exclidng this controller.

        Returns:
            A comma-separated list of controller numbers.
        """
        # INVOKE <id> Introspection.GetAppControllers
        # -> R:INVOKE <id> <rcode> Introspection.GetAppControllers <controllers>
        return await self.invoke("Introspection.GetAppControllers")

    @method("Introspection.GetFirmwareVersion")
    async def get_firmware_version(self, image: Firmware) -> FirmwareVersion:
        """Get the firmware version.

        Args:
            image: The firmware image to get the version of.
        """
        # INVOKE <id> Introspection.GetFirmwareVersion <image>
        # -> R:INVOKE <id> <rcode> Introspection.GetFirmwareVersion <image> <version>
        return await self.invoke("Introspection.GetFirmwareVersion", image)

    @method("Introspection.GetLicenseInfo")
    async def get_license_info(self, type: LicenseType) -> LicenseInfo:
        """Get license information.

        Args:
            type: The license type to get information for.
        """
        # INVOKE <id> Introspection.GetLicenseInfo <type>
        # -> R:INVOKE <id> <rcode> Introspection.GetLicenseInfo <type> <used> <total>
        return await self.invoke("Introspection.GetLicenseInfo", type)

    # Convenience functions, not part of the interface
    async def get_application_version(self) -> str:
        """Get the application firmware version."""
        response = await self.get_firmware_version(self.Firmware.APPLICATION)

        return response.version
