"""Interface for querying and controlling system objects."""

import datetime as dt

from .base import Interface


class ObjectInterface(Interface):
    """Interface for querying and controlling system objects."""

    method_signatures = {
        "Object.GetMTime": dt.datetime,
    }

    # Methods
    async def get_mtime(self) -> dt.datetime:
        """Get the modification time of an object.

        Returns:
            The modification time of the object, as a unix timestamp.
        """
        # INVOKE <id> Object.GetMTime
        # -> R:INVOKE <id> <mtime> Object.GetMTime
        return await self.invoke("Object.GetMTime")
