"""Interface for querying and controlling color temperature."""

from .base import Interface


class ColorTemperatureInterface(Interface):
    """Interface for querying and controlling color temperature."""

    method_signatures = {
        "ColorTemperature.Get": int,
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
        return await self.invoke(vid, "ColorTemperature.Get", as_type=int)
