"""Controller holding and managing Vantage controllers."""

from typing_extensions import override

from aiovantage.command_client.object_interfaces import IntrospectionInterface
from aiovantage.models import Master

from .base import BaseController


class MastersController(BaseController[Master], IntrospectionInterface):
    """Controller holding and managing Vantage controllers."""

    vantage_types = ("Master",)
    """The Vantage object types that this controller will fetch."""

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the state properties of a Vantage controller."""
        # TODO: IntrospectionInterface isn't available on firmware 2.x
        state = {
            "firmware_version": await IntrospectionInterface.get_firmware_version(
                self, vid, IntrospectionInterface.Firmware.Application
            ),
        }

        self.update_state(vid, state)
