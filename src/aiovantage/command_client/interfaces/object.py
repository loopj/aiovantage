from datetime import datetime
from typing import Sequence

from .base import Interface


class ObjectInterface(Interface):
    async def get_mtime(self, id: int) -> datetime:
        """
        Get the modification time of an object.

        Args:
            id: The ID of the object.

        Returns:
            The modification time of the object, as a datetime object.
        """

        # INVOKE <id> Object.GetMTime
        # -> R:INVOKE <id> <mtime> Object.GetMTime
        response = await self.invoke(id, "Object.GetMTime")
        mtime = datetime.fromtimestamp(int(response.args[1]))

        return mtime

    @classmethod
    def parse_get_mtime_status(cls, args: Sequence[str]) -> datetime:
        """
        Parse a "Object.GetMTime" event.

        Args:
            args: The arguments of the event.

        Returns:
            The modification time of the object, as a datetime object.
        """

        # ELLOG STATUS ON
        # -> EL: <id> Object.GetMTime <mtime>

        # STATUS ADD <id>
        # -> S:STATUS <id> Object.GetMTime <mtime>
        return datetime.fromtimestamp(int(args[0]))
