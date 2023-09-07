"""Interface for querying and controlling system objects."""

from .base import Interface, InterfaceResponse, int_result


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
        return self.parse_get_mtime_response(response)

    @classmethod
    def parse_get_mtime_response(cls, response: InterfaceResponse) -> int:
        """Parse a 'Object.GetMTime' response."""
        # -> R:INVOKE <id> <mtime> Object.GetMTime
        # -> S:STATUS <id> Object.GetMTime <mtime>
        # -> EL: <id> Object.GetMTime <mtime>
        return int_result(response)
