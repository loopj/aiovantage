"""Interface for querying and controlling color temperature."""

from .base import Interface, InterfaceResponse, int_result


class ColorTemperatureInterface(Interface):
    """Interface for querying and controlling color temperature."""

    async def get_color_temp(self, vid: int) -> int:
        """Get the color temperature of a light.

        Args:
            vid: The Vantage ID of the light.

        Returns:
            The color temperature of the light, in Kelvin.
        """
        # INVOKE <id> ColorTemperature.Get
        response = await self.invoke(vid, "ColorTemperature.Get")
        return self.parse_get_response(response)

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

    @classmethod
    def parse_get_response(cls, response: InterfaceResponse) -> int:
        """Parse a 'ColorTemperature.Get' response."""
        # -> R:INVOKE <id> <temp> ColorTemperature.Get
        # -> S:STATUS <id> ColorTemperature.Get <temp>
        # -> EL: <id> ColorTemperature.Get <temp>
        return int_result(response)
