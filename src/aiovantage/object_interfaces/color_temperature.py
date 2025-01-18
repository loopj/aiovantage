"""Interface for querying and controlling color temperature."""

from decimal import Decimal
from enum import IntEnum

from aiovantage.object_interfaces.interface_classes import WidgetPrecludable

from .base import Interface, method


class ColorTemperatureInterface(Interface, WidgetPrecludable):
    """Interface for querying and controlling color temperature."""

    interface_name = "ColorTemperature"

    # Types
    class Preset(IntEnum):
        """Color temperature preset."""

        NONE = 0
        SOFT = 2700
        WARM = 3000
        NEUTRAL = 3500
        COOL = 4100
        NATURAL = 5000
        DAYLIGHT = 6500

    # Properties
    color_temp: int | None = None
    max_value: int | None = None
    min_value: int | None = None

    # Methods
    @method("ColorTemperature.Set")
    @method("ColorTemperature.SetSW")
    async def set_temperature(
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

    @method("ColorTemperature.Get", property="color_temp")
    @method("ColorTemperature.GetHW")
    async def get_temperature(self, *, hw: bool = False) -> int:
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

    @method("ColorTemperature.StopTransition")
    async def stop_transition(self) -> None:
        """Stop any ongoing color temperature transitions."""
        # INVOKE <id> ColorTemperature.StopTransition
        # -> R:INVOKE <id> <rcode> ColorTemperature.StopTransition
        await self.invoke("ColorTemperature.StopTransition")

    @method("ColorTemperature.Warm")
    async def warm(self, amount: int, transition_time: float | Decimal) -> None:
        """Decrease the color temperature of a light.

        Args:
            amount: The amount to decrease the color temperature by.
            transition_time: The time in seconds to transition to the new color.
        """
        # INVOKE <id> ColorTemperature.Warm <amount> <transition_time>
        # -> R:INVOKE <id> <rcode> ColorTemperature.Warm <amount> <transition_time>
        await self.invoke("ColorTemperature.Warm", amount, transition_time)

    @method("ColorTemperature.Cool")
    async def cool(self, amount: int, transition_time: float | Decimal) -> None:
        """Increase the color temperature of a light.

        Args:
            amount: The amount to increase the color temperature by.
            transition_time: The time in seconds to transition to the new color.
        """
        # INVOKE <id> ColorTemperature.Cool <amount> <transition_time>
        # -> R:INVOKE <id> <rcode> ColorTemperature.Cool <amount> <transition_time>
        await self.invoke("ColorTemperature.Cool", amount, transition_time)

    @method("ColorTemperature.SetPreset")
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

    @method("ColorTemperature.GetPreset")
    async def get_temperature_preset(self) -> Preset:
        """Get the color temperature preset of a light.

        Returns:
            The color temperature preset of the light.
        """
        # INVOKE <id> ColorTemperature.GetPreset
        # -> R:INVOKE <id> <preset> ColorTemperature.GetPreset
        return await self.invoke("ColorTemperature.GetPreset")

    @method("ColorTemperature.GetMaxValue", property="max_value")
    @method("ColorTemperature.GetMaxValueHW")
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
            "ColorTemperature.GetMaxValueHW" if hw else "ColorTemperature.GetMaxValue"
        )

    @method("ColorTemperature.SetMaxValueSW")
    async def set_max_value(self, value: int) -> None:
        """Set the cached maximum color temperature of a light.

        Args:
            value: The maximum color temperature to set the light to, in Kelvin.
        """
        # INVOKE <id> ColorTemperature.SetMaxValueSW <value>
        # -> R:INVOKE <id> <rcode> ColorTemperature.SetMaxValueSW <value>
        await self.invoke("ColorTemperature.SetMaxValueSW", value)

    @method("ColorTemperature.GetMinValue", property="min_value")
    @method("ColorTemperature.GetMinValueHW")
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
            "ColorTemperature.GetMinValueHW" if hw else "ColorTemperature.GetMinValue"
        )

    @method("ColorTemperature.SetMinValueSW")
    async def set_min_value(self, value: int) -> None:
        """Set the cached minimum color temperature of a light.

        Args:
            value: The minimum color temperature to set the light to, in Kelvin.
        """
        # INVOKE <id> ColorTemperature.SetMinValueSW <value>
        # -> R:INVOKE <id> <rcode> ColorTemperature.SetMinValueSW <value>
        await self.invoke("ColorTemperature.SetMinValueSW", value)

    @method("ColorTemperature.GetTransitionTemperature")
    async def get_transition_temperature(self) -> int:
        """Get the current color temperature of a light in transition.

        Returns:
            The transition temperature of the light, in Kelvin.
        """
        # INVOKE <id> ColorTemperature.GetTransitionTemperature
        # -> R:INVOKE <id> <temp> ColorTemperature.GetTransitionTemperature
        return await self.invoke("ColorTemperature.GetTransitionTemperature")
