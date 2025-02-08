from dataclasses import dataclass, field
from enum import IntEnum

from .base import Interface, method


class IntrospectionInterface(Interface):
    """Introspection object interface."""

    interface_name = "Introspection"

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

    @dataclass
    class LicenseInfo:
        """A license info response."""

        used: int = field(metadata={"out": "arg1"})
        total: int = field(metadata={"out": "arg2"})

    # Methods
    @method("GetAppControllers", out="arg0")
    async def get_app_controllers(self) -> str:
        """Get a list of controllers in application mode, excluding this controller.

        Returns:
            A comma-separated list of controller numbers.
        """
        # INVOKE <id> Introspection.GetAppControllers
        # -> R:INVOKE <id> <rcode> Introspection.GetAppControllers <controllers>
        return await self.invoke("Introspection.GetAppControllers")

    @method("GetFirmwareVersion", out="arg1")
    async def get_firmware_version(self, image: Firmware) -> str:
        """Get the firmware version.

        Args:
            image: The firmware image to get the version of.
        """
        # INVOKE <id> Introspection.GetFirmwareVersion <image>
        # -> R:INVOKE <id> <rcode> Introspection.GetFirmwareVersion <image> <version>
        return await self.invoke("Introspection.GetFirmwareVersion", image)

    @method("GetLicenseInfo")
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
        return await self.get_firmware_version(self.Firmware.Application)
