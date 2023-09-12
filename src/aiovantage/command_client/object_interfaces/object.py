"""Interface for querying and controlling system objects."""

from .base import Interface
from .parsers import parse_int


class ObjectInterface(Interface):
    """Interface for querying and controlling system objects."""

    method_signatures = {
        "Object.GetMTime": parse_int,
    }

    async def get_mtime(self, vid: int) -> int:
        """Get the modification time of an object.

        Args:
            vid: The Vantage ID of the object.

        Returns:
            The modification time of the object, as a unix timestamp.
        """
        # INVOKE <id> Object.GetMTime
        # -> R:INVOKE <id> <mtime> Object.GetMTime
        return await self.invoke(vid, "Object.GetMTime", as_type=int)
