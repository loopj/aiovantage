from .base import Interface


class ColorTemperatureInterface(Interface):
    async def get_color_temp(self, id: int) -> int:
        """
        Get the color temperature of a light.

        Args:
            id: The ID of the light.

        Returns:
            The color temperature of the light, in Kelvin.
        """

        # INVOKE <id> ColorTemperature.Get
        # -> R:INVOKE <id> <temp> ColorTemperature.Get
        response = await self.invoke(id, "ColorTemperature.Get")
        color_temp = int(response.args[1])

        return color_temp

    async def set_color_temp(self, id: int, temp: int, transition: int = 0) -> None:
        """
        Set the color temperature of a light.

        Args:
            id: The ID of the light.
            temp: The color temperature to set the light to, in Kelvin.
            transition: The time in seconds to transition to the new color
        """

        # Ensure the temperature is an integer
        temp = int(temp)

        # INVOKE <id> ColorTemperature.Set <temp> <seconds>
        # -> R:INVOKE <id> <rcode> ColorTemperature.Set <temp>
        await self.invoke(id, "ColorTemperature.Set", temp, transition)
