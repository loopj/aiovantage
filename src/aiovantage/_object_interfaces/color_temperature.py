from decimal import Decimal
from enum import IntEnum

from .base import Interface, method


class ColorTemperatureInterface(Interface):
    """Interface for querying and controlling color temperature."""

    interface_name = "ColorTemperature"

    class Preset(IntEnum):
        """Color temperature preset."""

        None_ = 0
        Soft = 2700
        Warm = 3000
        Neutral = 3500
        Cool = 4100
        Natural = 5000
        Daylight = 6500

    # Properties
    color_temp: int | None = None
    max_value: int | None = None
    min_value: int | None = None

    # Methods
    @method("Set", "SetSW")
    async def set_color_temp(
        self, temp: int, transition: int = 0, *, sw: bool = False
    ) -> None:
        """Set the color temperature of a light.

        Args:
            temp: The color temperature to set the light to, in Kelvin.
            transition: The time in seconds to transition to the new color temperature.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> ColorTemperature.Set <temp> <seconds>
        # -> R:INVOKE <id> <rcode> ColorTemperature.Set <temp>
        await self.invoke(
            "ColorTemperature.SetSW" if sw else "ColorTemperature.Set", temp, transition
        )

    @method("Get", "GetHW", property="color_temp")
    async def get_color_temp(self, *, hw: bool = False) -> int:
        """Get the color temperature of a light.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The color temperature of the light, in Kelvin.
        """
        # INVOKE <id> ColorTemperature.Get
        # -> R:INVOKE <id> <temp> ColorTemperature.Get
        return await self.invoke(
            "ColorTemperature.GetHW" if hw else "ColorTemperature.Get"
        )

    @method("StopTransition")
    async def stop_transition(self) -> None:
        """Stop any ongoing color temperature transitions."""
        # INVOKE <id> ColorTemperature.StopTransition
        # -> R:INVOKE <id> <rcode> ColorTemperature.StopTransition
        await self.invoke("ColorTemperature.StopTransition")

    @method("Warm")
    async def warm(self, amount: int, transition_time: float | Decimal) -> None:
        """Decrease the color temperature of a light.

        Args:
            amount: The amount to decrease the color temperature by.
            transition_time: The time in seconds to transition to the new color.
        """
        # INVOKE <id> ColorTemperature.Warm <amount> <transition_time>
        # -> R:INVOKE <id> <rcode> ColorTemperature.Warm <amount> <transition_time>
        await self.invoke("ColorTemperature.Warm", amount, transition_time)

    @method("Cool")
    async def cool(self, amount: int, transition_time: float | Decimal) -> None:
        """Increase the color temperature of a light.

        Args:
            amount: The amount to increase the color temperature by.
            transition_time: The time in seconds to transition to the new color.
        """
        # INVOKE <id> ColorTemperature.Cool <amount> <transition_time>
        # -> R:INVOKE <id> <rcode> ColorTemperature.Cool <amount> <transition_time>
        await self.invoke("ColorTemperature.Cool", amount, transition_time)

    @method("SetPreset")
    async def set_temperature_preset(
        self, value: Preset, transition_time: float | Decimal
    ) -> None:
        """Set the color temperature of a light to a preset value.

        Args:
            value: The preset value to set the light to.
            transition_time: The time in seconds to transition to the new color.
        """
        # INVOKE <id> ColorTemperature.SetPreset <value> <transition_time>
        # -> R:INVOKE <id> <rcode> ColorTemperature.SetPreset <value> <transition_time>
        await self.invoke("ColorTemperature.SetPreset", value, transition_time)

    @method("GetPreset")
    async def get_temperature_preset(self) -> Preset:
        """Get the color temperature preset of a light.

        Returns:
            The color temperature preset of the light.
        """
        # INVOKE <id> ColorTemperature.GetPreset
        # -> R:INVOKE <id> <preset> ColorTemperature.GetPreset
        return await self.invoke("ColorTemperature.GetPreset")

    @method("GetMaxValue", "GetMaxValueHW", property="max_value")
    async def get_max_value(self, *, hw: bool = False) -> int:
        """Get the maximum color temperature of a light.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The maximum color temperature of the light, in Kelvin.
        """
        # INVOKE <id> ColorTemperature.GetMaxValue
        # -> R:INVOKE <id> <temp> ColorTemperature.GetMaxValue
        return await self.invoke(
            "ColorTemperature.GetMaxValueHW" if hw else "ColorTemperature.GetMaxValue",
        )

    @method("SetMaxValueSW")
    async def set_max_value(self, value: int) -> None:
        """Set the cached maximum color temperature of a light.

        Args:
            value: The maximum color temperature to set the light to, in Kelvin.
        """
        # INVOKE <id> ColorTemperature.SetMaxValueSW <value>
        # -> R:INVOKE <id> <rcode> ColorTemperature.SetMaxValueSW <value>
        await self.invoke("ColorTemperature.SetMaxValueSW", value)

    @method("GetMinValue", "GetMinValueHW", property="min_value")
    async def get_min_value(self, *, hw: bool = False) -> int:
        """Get the minimum color temperature of a light.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The minimum color temperature of the light, in Kelvin.
        """
        # INVOKE <id> ColorTemperature.GetMinValue
        # -> R:INVOKE <id> <temp> ColorTemperature.GetMinValue
        return await self.invoke(
            "ColorTemperature.GetMinValueHW" if hw else "ColorTemperature.GetMinValue",
        )

    @method("SetMinValueSW")
    async def set_min_value(self, value: int) -> None:
        """Set the cached minimum color temperature of a light.

        Args:
            value: The minimum color temperature to set the light to, in Kelvin.
        """
        # INVOKE <id> ColorTemperature.SetMinValueSW <value>
        # -> R:INVOKE <id> <rcode> ColorTemperature.SetMinValueSW <value>
        await self.invoke("ColorTemperature.SetMinValueSW", value)

    @method("GetTransitionTemperature")
    async def get_transition_temperature(self) -> int:
        """Get the current color temperature of a light in transition.

        Returns:
            The transition temperature of the light, in Kelvin.
        """
        # INVOKE <id> ColorTemperature.GetTransitionTemperature
        # -> R:INVOKE <id> <temp> ColorTemperature.GetTransitionTemperature
        return await self.invoke("ColorTemperature.GetTransitionTemperature")
