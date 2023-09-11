"""Interface for querying and controlling color temperature."""

from .base import Interface
from .parsers import parse_int


class ColorTemperatureInterface(Interface):
    """Interface for querying and controlling color temperature."""

    response_parsers = {
        "ColorTemperature.Get": parse_int,
    }

    async def set_color_temp(self, vid: int, temp: int, transition: int = 0) -> None:
        """Set the color temperature of a light.

        Args:
            vid: The Vantage ID of the light.
            temp: The color temperature to set the light to, in Kelvin.
            transition: The time in seconds to transition to the new color
        """
        # INVOKE <id> ColorTemperature.Set <temp> <seconds>
        # -> R:INVOKE <id> <rcode> ColorTemperature.Set <temp>
        await self.invoke(vid, "ColorTemperature.Set", temp, transition)

    async def get_color_temp(self, vid: int) -> int:
        """Get the color temperature of a light.

        Args:
            vid: The Vantage ID of the light.

        Returns:
            The color temperature of the light, in Kelvin.
        """
        # INVOKE <id> ColorTemperature.Get
        # -> R:INVOKE <id> <temp> ColorTemperature.Get
        response = await self.invoke(vid, "ColorTemperature.Get")
        return ColorTemperatureInterface.parse_response(response, int)
