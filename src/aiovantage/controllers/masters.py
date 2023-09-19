"""Controller holding and managing Vantage controllers."""

from contextlib import suppress

from typing_extensions import override

from aiovantage.command_client.object_interfaces import IntrospectionInterface
from aiovantage.errors import CommandError
from aiovantage.models import Master

from .base import BaseController


class MastersController(BaseController[Master], IntrospectionInterface):
    """Controller holding and managing Vantage controllers."""

    vantage_types = ("Master",)
    """The Vantage object types that this controller will fetch."""

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the state properties of a Vantage controller."""
        state = {}

        # IntrospectionInterface is not available on 2.x firmware.
        with suppress(CommandError):
            state[
                "firmware_version"
            ] = await IntrospectionInterface.get_firmware_version(
                self, vid, self.Firmware.Application
            )

        self.update_state(vid, state)
