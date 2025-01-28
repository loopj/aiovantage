"""Controller holding and managing Vantage variables."""

from typing_extensions import override

from aiovantage.objects import GMem

from .base import BaseController


class GMemController(BaseController[GMem]):
    """Controller holding and managing Vantage variables.

    We use the `GETVARIABLE` and `VARIABLE` wrappers for getting and setting
    variable values, rather than the GMem object interface, since they are much
    simpler than working with raw byte arrays.
    """

    vantage_types = ("GMem",)
    """The Vantage object types that this controller will fetch."""

    status_types = ("VARIABLE",)
    """Which Vantage 'STATUS' types this controller handles, if any."""

    @override
    async def fetch_object_state(self, obj: GMem) -> None:
        """Fetch the state properties of a variable."""
        state = {
            "value": await obj.get_value(),
        }

        self.update_state(obj, state)

    @override
    def handle_status(self, obj: GMem, status: str, *args: str) -> None:
        """Handle simple status messages from the event stream."""
        if status != "VARIABLE":
            return

        # STATUS VARIABLE
        # -> S:VARIABLE <id> <value>
        state = {
            "value": obj.parse_value(args[0]),
        }

        self.update_state(obj, state)
