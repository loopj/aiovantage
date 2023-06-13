from typing import Sequence

from .base import Interface


class SensorInterface(Interface):
    async def get_level(self, id: int) -> int:
        """
        Get the level of a sensor.

        Args:
            id: The ID of the sensor.
        """

        # INVOKE <id> Sensor.GetLevel
        # -> R:INVOKE <id> <level (0-100)> Sensor.GetLevel
        response = await self.invoke(id, "Sensor.GetLevel")
        level = int(response.args[1])

        return level

    @classmethod
    def parse_get_level_status(cls, args: Sequence[str]) -> int:
        """
        Parse a "Sensor.GetLevel" event.

        Args:
            args: The arguments of the event.

        Returns:
            The level of the sensor.
        """

        # ELLOG STATUS ON
        # -> EL: <id> Sensor.GetLevel <level>

        # STATUS ADD <id>
        # -> S:STATUS <id> Sensor.GetLevel <level>
        return int(args[0])