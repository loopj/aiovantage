"""Interface for controller introspection."""

from enum import IntEnum
from typing import NamedTuple

from .base import Interface


class IntrospectionInterface(Interface):
    """Interface for controller introspection."""

    class Firmware(IntEnum):
        """Firmware image."""

        Kernel = 0
        RootFs = 1
        Application = 2

    class LicenseType(IntEnum):
        """License type."""

        Unknown = 0
        Equinox = 1
        All = -1

    class FirmwareVersion(NamedTuple):
        """A firmware version response."""

        rcode: int
        image: "IntrospectionInterface.Firmware"
        version: str
        size: int

    class LicenseInfo(NamedTuple):
        """A license info response."""

        rcode: int
        type: "IntrospectionInterface.LicenseType"
        used: int
        total: int

    method_signatures = {
        "Introspection.GetAppControllers": str,
        "Introspection.GetFirmwareVersion": FirmwareVersion,
        "Introspection.GetLicenseInfo": LicenseInfo,
    }

    async def get_app_controllers(self, vid: int) -> str:
        """Get a list of controllers in application mode, exclidng this controller.

        Args:
            vid: The Vantage ID of the controller.

        Returns:
            A comma-separated list of controller numbers.
        """
        # INVOKE <id> Introspection.GetAppControllers
        # -> R:INVOKE <id> <rcode> Introspection.GetAppControllers <controllers>
        return await self.invoke(vid, "Introspection.GetAppControllers")

    async def get_firmware_version(self, vid: int, image: Firmware) -> FirmwareVersion:
        """Get the firmware version.

        Args:
            vid: The Vantage ID of the controller.
            image: The firmware image to get the version of.
        """
        # INVOKE <id> Introspection.GetFirmwareVersion <image>
        # -> R:INVOKE <id> <rcode> Introspection.GetFirmwareVersion <image> <version>
        return await self.invoke(vid, "Introspection.GetFirmwareVersion", image)

    async def get_license_info(self, vid: int, type: LicenseType) -> LicenseInfo:
        """Get license information.

        Args:
            vid: The Vantage ID of the controller.
            type: The license type to get information for.
        """
        # INVOKE <id> Introspection.GetLicenseInfo <type>
        # -> R:INVOKE <id> <rcode> Introspection.GetLicenseInfo <type> <used> <total>
        return await self.invoke(vid, "Introspection.GetLicenseInfo", type)

    # Convenience functions, not part of the interface
    async def get_application_version(self, vid: int) -> str:
        """Get the application firmware version."""
        response = await self.get_firmware_version(vid, self.Firmware.Application)

        return response.version
