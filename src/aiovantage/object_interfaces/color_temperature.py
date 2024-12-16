"""Interface for querying and controlling color temperature."""

from aiovantage.object_interfaces.base import Interface


class ColorTemperatureInterface(Interface):
    """Interface for querying and controlling color temperature."""

    method_signatures = {
        "ColorTemperature.Get": int,
    }

    # Properties
    color_temp: int | None = None
    max_value: int | None = None
    min_value: int | None = None

    # Methods
    async def set_color_temp(self, temp: int, transition: int = 0) -> None:
        """Set the color temperature of a light.

        Args:
            temp: The color temperature to set the light to, in Kelvin.
            transition: The time in seconds to transition to the new color
        """
        # INVOKE <id> ColorTemperature.Set <temp> <seconds>
        # -> R:INVOKE <id> <rcode> ColorTemperature.Set <temp>
        await self.invoke("ColorTemperature.Set", temp, transition)

    async def get_color_temp(self) -> int:
        """Get the color temperature of a light.

        Returns:
            The color temperature of the light, in Kelvin.
        """
        # INVOKE <id> ColorTemperature.Get
        # -> R:INVOKE <id> <temp> ColorTemperature.Get
        return await self.invoke("ColorTemperature.Get", as_type=int)
