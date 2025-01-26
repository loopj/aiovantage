"""Interface for querying and controlling color temperature."""

from decimal import Decimal
from enum import IntEnum

from .base import Interface


class ColorTemperatureInterface(Interface):
    """Interface for querying and controlling color temperature."""

    class Preset(IntEnum):
        """Color temperature preset."""

        None_ = 0
        Soft = 2700
        Warm = 3000
        Neutral = 3500
        Cool = 4100
        Natural = 5000
        Daylight = 6500

    method_signatures = {
        "ColorTemperature.Get": int,
        "ColorTemperature.GetHW": int,
        "ColorTemperature.GetPreset": Preset,
        "ColorTemperature.GetMaxValue": int,
        "ColorTemperature.GetMaxValueHW": int,
        "ColorTemperature.GetMinValue": int,
        "ColorTemperature.GetMinValueHW": int,
        "ColorTemperature.GetTransitionTemperature": int,
    }

    async def set_color_temp(
        self, vid: int, temp: int, transition: int = 0, *, sw: bool = False
    ) -> None:
        """Set the color temperature of a light.

        Args:
            vid: The Vantage ID of the light.
            temp: The color temperature to set the light to, in Kelvin.
            transition: The time in seconds to transition to the new color temperature.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> ColorTemperature.Set <temp> <seconds>
        # -> R:INVOKE <id> <rcode> ColorTemperature.Set <temp>
        await self.invoke(
            vid,
            "ColorTemperature.SetSW" if sw else "ColorTemperature.Set",
            temp,
            transition,
        )

    async def get_color_temp(self, vid: int, *, hw: bool = False) -> int:
        """Get the color temperature of a light.

        Args:
            vid: The Vantage ID of the light.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The color temperature of the light, in Kelvin.
        """
        # INVOKE <id> ColorTemperature.Get
        # -> R:INVOKE <id> <temp> ColorTemperature.Get
        return await self.invoke(
            vid, "ColorTemperature.GetHW" if hw else "ColorTemperature.Get"
        )

    async def stop_transition(self, vid: int) -> None:
        """Stop any ongoing color temperature transitions.

        Args:
            vid: The Vantage ID of the light.
        """
        # INVOKE <id> ColorTemperature.StopTransition
        # -> R:INVOKE <id> <rcode> ColorTemperature.StopTransition
        await self.invoke(vid, "ColorTemperature.StopTransition")

    async def warm(
        self, vid: int, amount: int, transition_time: float | Decimal
    ) -> None:
        """Decrease the color temperature of a light.

        Args:
            vid: The Vantage ID of the light.
            amount: The amount to decrease the color temperature by.
            transition_time: The time in seconds to transition to the new color.
        """
        # INVOKE <id> ColorTemperature.Warm <amount> <transition_time>
        # -> R:INVOKE <id> <rcode> ColorTemperature.Warm <amount> <transition_time>
        await self.invoke(vid, "ColorTemperature.Warm", amount, transition_time)

    async def cool(
        self, vid: int, amount: int, transition_time: float | Decimal
    ) -> None:
        """Increase the color temperature of a light.

        Args:
            vid: The Vantage ID of the light.
            amount: The amount to increase the color temperature by.
            transition_time: The time in seconds to transition to the new color.
        """
        # INVOKE <id> ColorTemperature.Cool <amount> <transition_time>
        # -> R:INVOKE <id> <rcode> ColorTemperature.Cool <amount> <transition_time>
        await self.invoke(vid, "ColorTemperature.Cool", amount, transition_time)

    async def set_temperature_preset(
        self, vid: int, value: Preset, transition_time: float | Decimal
    ) -> None:
        """Set the color temperature of a light to a preset value.

        Args:
            vid: The Vantage ID of the light.
            value: The preset value to set the light to.
            transition_time: The time in seconds to transition to the new color.
        """
        # INVOKE <id> ColorTemperature.SetPreset <value> <transition_time>
        # -> R:INVOKE <id> <rcode> ColorTemperature.SetPreset <value> <transition_time>
        await self.invoke(vid, "ColorTemperature.SetPreset", value, transition_time)

    async def get_temperature_preset(self, vid: int) -> Preset:
        """Get the color temperature preset of a light.

        Args:
            vid: The Vantage ID of the light.

        Returns:
            The color temperature preset of the light.
        """
        # INVOKE <id> ColorTemperature.GetPreset
        # -> R:INVOKE <id> <preset> ColorTemperature.GetPreset
        return await self.invoke(vid, "ColorTemperature.GetPreset")

    async def get_max_value(self, vid: int, *, hw: bool = False) -> int:
        """Get the maximum color temperature of a light.

        Args:
            vid: The Vantage ID of the light.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The maximum color temperature of the light, in Kelvin.
        """
        # INVOKE <id> ColorTemperature.GetMaxValue
        # -> R:INVOKE <id> <temp> ColorTemperature.GetMaxValue
        return await self.invoke(
            vid,
            "ColorTemperature.GetMaxValueHW" if hw else "ColorTemperature.GetMaxValue",
        )

    async def set_max_value(self, vid: int, value: int) -> None:
        """Set the cached maximum color temperature of a light.

        Args:
            vid: The Vantage ID of the light.
            value: The maximum color temperature to set the light to, in Kelvin.
        """
        # INVOKE <id> ColorTemperature.SetMaxValueSW <value>
        # -> R:INVOKE <id> <rcode> ColorTemperature.SetMaxValueSW <value>
        await self.invoke(vid, "ColorTemperature.SetMaxValueSW", value)

    async def get_min_value(self, vid: int, *, hw: bool = False) -> int:
        """Get the minimum color temperature of a light.

        Args:
            vid: The Vantage ID of the light.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The minimum color temperature of the light, in Kelvin.
        """
        # INVOKE <id> ColorTemperature.GetMinValue
        # -> R:INVOKE <id> <temp> ColorTemperature.GetMinValue
        return await self.invoke(
            vid,
            "ColorTemperature.GetMinValueHW" if hw else "ColorTemperature.GetMinValue",
        )

    async def set_min_value(self, vid: int, value: int) -> None:
        """Set the cached minimum color temperature of a light.

        Args:
            vid: The Vantage ID of the light.
            value: The minimum color temperature to set the light to, in Kelvin.
        """
        # INVOKE <id> ColorTemperature.SetMinValueSW <value>
        # -> R:INVOKE <id> <rcode> ColorTemperature.SetMinValueSW <value>
        await self.invoke(vid, "ColorTemperature.SetMinValueSW", value)

    async def get_transition_temperature(self, vid: int) -> int:
        """Get the current color temperature of a light in transition.

        Args:
            vid: The Vantage ID of the light.

        Returns:
            The transition temperature of the light, in Kelvin.
        """
        # INVOKE <id> ColorTemperature.GetTransitionTemperature
        # -> R:INVOKE <id> <temp> ColorTemperature.GetTransitionTemperature
        return await self.invoke(vid, "ColorTemperature.GetTransitionTemperature")
