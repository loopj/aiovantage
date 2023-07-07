"""Interface for querying and controlling system objects."""

from typing import Sequence

from .base import Interface


class ObjectInterface(Interface):
    """Interface for querying and controlling system objects."""

    async def get_mtime(self, vid: int) -> int:
        """Get the modification time of an object.

        Args:
            vid: The Vantage ID of the object.

        Returns:
            The modification time of the object, as a unix timestamp.
        """
        # INVOKE <id> Object.GetMTime
        # -> R:INVOKE <id> <mtime> Object.GetMTime
        response = await self.invoke(vid, "Object.GetMTime")
        mtime = int(response.args[1])

        return mtime

    @classmethod
    def parse_get_mtime_status(cls, args: Sequence[str]) -> int:
        """Parse an 'Object.GetMTime' event.

        Args:
            args: The arguments of the event.

        Returns:
            The modification time of the object, as a unix timestamp.
        """
        # ELLOG STATUS ON
        # -> EL: <id> Object.GetMTime <mtime>
        # STATUS ADD <id>
        # -> S:STATUS <id> Object.GetMTime <mtime>
        return int(args[0])
