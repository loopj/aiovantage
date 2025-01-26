"""Interface for querying and controlling RGB loads."""

from decimal import Decimal
from enum import IntEnum
from itertools import islice

from .base import Interface


class RGBLoadInterface(Interface):
    """Interface for querying and controlling RGB loads."""

    class RGBChannel(IntEnum):
        """The RGB color channels."""

        Red = 0
        Green = 1
        Blue = 2
        White = 3

    class HSLAttribute(IntEnum):
        """The HSL color attributes."""

        Hue = 0
        Saturation = 1
        Lightness = 2

    class ColorName(IntEnum):
        """Color."""

        Unknown = 0
        White = 1
        Red = 2
        Yellow = 3
        Green = 4
        Magenta = 5
        Blue = 6
        Cyan = 7

    method_signatures = {
        "RGBLoad.GetRGB": int,
        "RGBLoad.GetRGBHW": int,
        "RGBLoad.GetHSL": int,
        "RGBLoad.GetHSLHW": int,
        "RGBLoad.GetDissolveRate": Decimal,
        "RGBLoad.GetDissolveRateHW": Decimal,
        "RGBLoad.GetPreset": int,
        "RGBLoad.GetPresetHW": int,
        "RGBLoad.GetEffect": int,
        "RGBLoad.GetEffectHW": int,
        "RGBLoad.GetColorName": ColorName,
        "RGBLoad.GetColor": int,
        "RGBLoad.GetColorHW": int,
        "RGBLoad.GetRGBW": int,
        "RGBLoad.GetRGBWHW": int,
        "RGBLoad.GetTransitionLevel": Decimal,
    }

    async def set_rgb(
        self,
        vid: int,
        red: int = 255,
        green: int = 255,
        blue: int = 255,
        *,
        sw: bool = False,
    ) -> None:
        """Set the color of an RGB load.

        Args:
            vid: The Vantage ID of the load.
            red: The red value of the color, (0-255)
            green: The green value of the color, (0-255)
            blue: The blue value of the color, (0-255)
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> RGBLoad.SetRGB <red> <green> <blue>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGB <red> <green> <blue>
        await self.invoke(
            vid, "RGBLoad.SetRGBSW" if sw else "RGBLoad.SetRGB", red, green, blue
        )

    async def get_rgb(self, vid: int, channel: RGBChannel, *, hw: bool = False) -> int:
        """Get a single RGB color channel of a load from the controller.

        Args:
            vid: The Vantage ID of the load.
            channel: The channel to get the color of.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The value of the RGB channel, 0-255.
        """
        # INVOKE <id> RGBLoad.GetRGB <channel>
        # -> R:INVOKE <id> <value> RGBLoad.GetRGB <channel>
        return await self.invoke(
            vid, "RGBLoad.GetRGBHW" if hw else "RGBLoad.GetRGB", channel
        )

    async def set_hsl(
        self,
        vid: int,
        hue: int,
        saturation: float | Decimal,
        lightness: float | Decimal,
        *,
        sw: bool = False,
    ) -> None:
        """Set the color of an HSL load.

        Args:
            vid: The Vantage ID of the load.
            hue: The hue value of the color, in degrees (0-360).
            saturation: The saturation value of the color, in percent (0-100).
            lightness: The lightness value of the color, in percent (0-100).
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> RGBLoad.SetHSL <hue> <saturation> <lightness>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetHSL <hue> <saturation> <lightness>
        await self.invoke(
            vid,
            "RGBLoad.SetHSLSW" if sw else "RGBLoad.SetHSL",
            hue,
            saturation,
            lightness,
        )

    async def get_hsl(
        self, vid: int, attribute: HSLAttribute, *, hw: bool = False
    ) -> int:
        """Get a single HSL color attribute of a load from the controller.

        Args:
            vid: The Vantage ID of the load.
            attribute: The attribute to get the value of.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The value of the HSL attribute, 0-360 for hue, 0-100 for saturation and
            lightness.
        """
        # INVOKE <id> RGBLoad.GetHSL <attribute>
        # -> R:INVOKE <id> <value> RGBLoad.GetHSL <attribute>
        return await self.invoke(
            vid, "RGBLoad.GetHSLHW" if hw else "RGBLoad.GetHSL", attribute
        )

    async def dissolve_rgb(
        self, vid: int, red: int, green: int, blue: int, rate: float | Decimal
    ) -> None:
        """Transition the color of an RGB load over a number of seconds.

        Args:
            vid: The Vantage ID of the load.
            red: The new red value of the color, (0-255)
            green: The new green value of the color, (0-255)
            blue: The new blue value of the color, (0-255)
            rate: The number of seconds the transition should take.
        """
        # INVOKE <id> RGBLoad.DissolveRGB <red> <green> <blue> <rate>
        # -> R:INVOKE <id> <rcode> RGBLoad.DissolveRGB <red> <green> <blue> <rate>
        await self.invoke(vid, "RGBLoad.DissolveRGB", red, green, blue, rate)

    async def dissolve_hsl(
        self,
        vid: int,
        hue: int,
        saturation: float | Decimal,
        lightness: float | Decimal,
        rate: float | Decimal,
    ) -> None:
        """Transition the color of an HSL load over a number of seconds.

        Args:
            vid: The Vantage ID of the load.
            hue: The new hue value of the color, in degrees (0-360).
            saturation: The new saturation value of the color, in percent (0-100).
            lightness: The new lightness value of the color, in percent (0-100).
            rate: The number of seconds the transition should take.
        """
        # INVOKE <id> RGBLoad.DissolveHSL <hue> <saturation> <lightness> <rate>
        # -> R:INVOKE <id> <rcode> RGBLoad.DissolveHSL <hue> <saturation> <lightness> <rate>
        await self.invoke(vid, "RGBLoad.DissolveHSL", hue, saturation, lightness, rate)

    async def set_dissolve_rate(
        self, vid: int, rate: float | Decimal, *, sw: bool = False
    ) -> None:
        """Set the default dissolve rate for RGB and HSL transitions.

        Args:
            vid: The Vantage ID of the load.
            rate: The number of seconds the transition should take.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> RGBLoad.SetDissolveRate <rate>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetDissolveRate <rate>
        await self.invoke(
            vid, "RGBLoad.SetDissolveRateSW" if sw else "RGBLoad.SetDissolveRate", rate
        )

    async def get_dissolve_rate(self, vid: int, *, hw: bool = False) -> Decimal:
        """Get the default dissolve rate for RGB and HSL transitions.

        Args:
            vid: The Vantage ID of the load.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The number of seconds the transition should take.
        """
        # INVOKE <id> RGBLoad.GetDissolveRate
        # -> R:INVOKE <id> <rate> RGBLoad.GetDissolveRate
        return await self.invoke(
            vid, "RGBLoad.GetDissolveRateHW" if hw else "RGBLoad.GetDissolveRate"
        )

    async def increment_rgb_component(self, vid: int, channel: RGBChannel) -> None:
        """Increment a single RGB color channel of a load.

        Args:
            vid: The Vantage ID of the load.
            channel: The channel to increment the color of.
        """
        # INVOKE <id> RGBLoad.IncrementRGBComponent <channel>
        # -> R:INVOKE <id> <rcode> RGBLoad.IncrementRGBComponent <channel>
        await self.invoke(vid, "RGBLoad.IncrementRGBComponent", channel)

    async def decrement_rgb_component(self, vid: int, channel: RGBChannel) -> None:
        """Decrement a single RGB color channel of a load.

        Args:
            vid: The Vantage ID of the load.
            channel: The channel to decrement the color of.
        """
        # INVOKE <id> RGBLoad.DecrementRGBComponent <channel>
        # -> R:INVOKE <id> <rcode> RGBLoad.DecrementRGBComponent <channel>
        await self.invoke(vid, "RGBLoad.DecrementRGBComponent", channel)

    async def set_rgb_component(
        self, vid: int, channel: RGBChannel, value: int
    ) -> None:
        """Set a single RGB(W) color channel of a load.

        Args:
            vid: The Vantage ID of the load.
            channel: The channel to set the color of.
            value: The value to set the channel to, 0-255.
        """
        # INVOKE <id> RGBLoad.SetRGBComponent <channel> <value>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGBComponent <channel> <value>
        await self.invoke(vid, "RGBLoad.SetRGBComponent", channel, value)

    async def increment_hsl_attribute(self, vid: int, attribute: HSLAttribute) -> None:
        """Increment a single HSL color attribute of a load.

        Args:
            vid: The Vantage ID of the load.
            attribute: The attribute to increment the value of.
        """
        # INVOKE <id> RGBLoad.IncrementHSLAttribute <attribute>
        # -> R:INVOKE <id> <rcode> RGBLoad.IncrementHSLAttribute <attribute>
        await self.invoke(vid, "RGBLoad.IncrementHSLAttribute", attribute)

    async def decrement_hsl_attribute(self, vid: int, attribute: HSLAttribute) -> None:
        """Decrement a single HSL color attribute of a load.

        Args:
            vid: The Vantage ID of the load.
            attribute: The attribute to decrement the value of.
        """
        # INVOKE <id> RGBLoad.DecrementHSLAttribute <attribute>
        # -> R:INVOKE <id> <rcode> RGBLoad.DecrementHSLAttribute <attribute>
        await self.invoke(vid, "RGBLoad.DecrementHSLAttribute", attribute)

    async def set_hsl_attribute(
        self, vid: int, attribute: HSLAttribute, value: int
    ) -> None:
        """Set a single HSL color attribute of a load.

        Args:
            vid: The Vantage ID of the load.
            attribute: The attribute to set the value of.
            value: The value to set the attribute to, 0-360 for hue, 0-100 for
                saturation and lightness.
        """
        # INVOKE <id> RGBLoad.SetHSLAttribute <attribute> <value>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetHSLAttribute <attribute> <value>
        await self.invoke(vid, "RGBLoad.SetHSLAttribute", attribute, value)

    async def stop(self, vid: int) -> None:
        """Stop the transition.

        Args:
            vid: The Vantage ID of the load.
        """
        # INVOKE <id> RGBLoad.Stop
        # -> R:INVOKE <id> <rcode> RGBLoad.Stop
        await self.invoke(vid, "RGBLoad.Stop")

    async def next_preset(self, vid: int) -> None:
        """Change to the next lighting preset.

        Args:
            vid: The Vantage ID of the load.
        """
        # INVOKE <id> RGBLoad.NextPreset
        # -> R:INVOKE <id> <rcode> RGBLoad.NextPreset
        await self.invoke(vid, "RGBLoad.NextPreset")

    async def previous_preset(self, vid: int) -> None:
        """Change to the previous lighting preset.

        Args:
            vid: The Vantage ID of the load.
        """
        # INVOKE <id> RGBLoad.PreviousPreset
        # -> R:INVOKE <id> <rcode> RGBLoad.PreviousPreset
        await self.invoke(vid, "RGBLoad.PreviousPreset")

    async def next_effect(self, vid: int) -> None:
        """Change to the next lighting effect.

        Args:
            vid: The Vantage ID of the load.
        """
        # INVOKE <id> RGBLoad.NextEffect
        # -> R:INVOKE <id> <rcode> RGBLoad.NextEffect
        await self.invoke(vid, "RGBLoad.NextEffect")

    async def previous_effect(self, vid: int) -> None:
        """Change to the previous lighting effect.

        Args:
            vid: The Vantage ID of the load.
        """
        # INVOKE <id> RGBLoad.PreviousEffect
        # -> R:INVOKE <id> <rcode> RGBLoad.PreviousEffect
        await self.invoke(vid, "RGBLoad.PreviousEffect")

    async def set_preset(self, vid: int, index: int, *, sw: bool = False) -> None:
        """Change to a specific lighting preset.

        Args:
            vid: The Vantage ID of the load.
            index: The index of the preset to change to.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> RGBLoad.SetPreset <index>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetPreset <index>
        await self.invoke(
            vid, "RGBLoad.SetPresetSW" if sw else "RGBLoad.SetPreset", index
        )

    async def get_preset(self, vid: int, *, hw: bool = False) -> int:
        """Get the current lighting preset.

        Args:
            vid: The Vantage ID of the load.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The index of the current preset.
        """
        # INVOKE <id> RGBLoad.GetPreset
        # -> R:INVOKE <id> <index> RGBLoad.GetPreset
        return await self.invoke(
            vid, "RGBLoad.GetPresetHW" if hw else "RGBLoad.GetPreset"
        )

    async def set_effect(self, vid: int, index: int, *, sw: bool = False) -> None:
        """Change to a specific lighting effect.

        Args:
            vid: The Vantage ID of the load.
            index: The index of the effect to change to.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> RGBLoad.SetEffect <index>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetEffect <index>
        await self.invoke(
            vid, "RGBLoad.SetEffectSW" if sw else "RGBLoad.SetEffect", index
        )

    async def get_effect(self, vid: int, *, hw: bool = False) -> int:
        """Get the current lighting effect.

        Args:
            vid: The Vantage ID of the load.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The index of the current effect.
        """
        # INVOKE <id> RGBLoad.GetEffect
        # -> R:INVOKE <id> <index> RGBLoad.GetEffect
        return await self.invoke(
            vid, "RGBLoad.GetEffectHW" if hw else "RGBLoad.GetEffect"
        )

    async def set_color_by_name(self, vid: int, color: ColorName) -> None:
        """Set the color of an RGB load by name.

        Args:
            vid: The Vantage ID of the load.
            color: The name of the color to set the load to.
        """
        # INVOKE <id> RGBLoad.SetColorByName <color>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetColorByName <color>
        await self.invoke(vid, "RGBLoad.SetColorByName", color)

    async def get_color_name(self, vid: int) -> ColorName:
        """Get the name of the color of a load from the controller.

        Args:
            vid: The Vantage ID of the load.

        Returns:
            The name of the color.
        """
        # INVOKE <id> RGBLoad.GetColorName
        # -> R:INVOKE <id> <color> RGBLoad.GetColorName
        return await self.invoke(vid, "RGBLoad.GetColorName")

    async def get_color(self, vid: int, *, hw: bool = False) -> int:
        """Get the RGB/RGBW color of a load from the controller.

        Args:
            vid: The Vantage ID of the load.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The RGB(W) value of the color as a packed big-endian integer.
        """
        # To unpack the response:
        # response.to_bytes(4, byteorder='big', signed=True)
        # NOTE: The W value always seems to be 0, even for RGBW loads.

        # INVOKE <id> RGBLoad.GetColor
        # -> R:INVOKE <id> <color> RGBLoad.GetColor
        return await self.invoke(
            vid, "RGBLoad.GetColorHW" if hw else "RGBLoad.GetColor"
        )

    async def set_rgbw(
        self,
        vid: int,
        red: int = 255,
        green: int = 255,
        blue: int = 255,
        white: int = 255,
        *,
        sw: bool = False,
    ) -> None:
        """Set the color of an RGBW load.

        Args:
            vid: The Vantage ID of the load.
            red: The red value of the color, (0-255)
            green: The green value of the color, (0-255)
            blue: The blue value of the color, (0-255)
            white: The white value of the color, (0-255)
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> RGBLoad.SetRGBW <red> <green> <blue> <white>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGBW <red> <green> <blue> <white>
        await self.invoke(
            vid,
            "RGBLoad.SetRGBWSW" if sw else "RGBLoad.SetRGBW",
            red,
            green,
            blue,
            white,
        )

    async def get_rgbw(self, vid: int, channel: int, *, hw: bool = False) -> int:
        """Get a single RGBW color channel of a load from the controller.

        Args:
            vid: The Vantage ID of the load.
            channel: The channel to get the color of.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The value of the RGBW channel, 0-255.
        """
        # INVOKE <id> RGBLoad.GetRGBW <channel>
        # -> R:INVOKE <id> <value> RGBLoad.GetRGBW <channel>
        return await self.invoke(
            vid, "RGBLoad.GetRGBWHW" if hw else "RGBLoad.GetRGBW", channel
        )

    async def get_transition_level(self, vid: int) -> Decimal:
        """Get the transition level of a load.

        Args:
            vid: The Vantage ID of the load.

        Returns:
            The transition level of the load.
        """
        # INVOKE <id> RGBLoad.GetTransitionLevel
        # -> R:INVOKE <id> <level> RGBLoad.GetTransitionLevel
        return await self.invoke(vid, "RGBLoad.GetTransitionLevel")

    # Convenience functions, not part of the interface
    async def get_rgb_color(self, vid: int) -> tuple[int, ...]:
        """Get the RGB color of a load from the controller.

        Returns:
            The value of the RGB color as a tuple of (red, green, blue).
        """
        return tuple(
            [await self.get_rgb(vid, chan) for chan in islice(self.RGBChannel, 3)]
        )

    async def get_rgbw_color(self, vid: int) -> tuple[int, ...]:
        """Get the RGBW color of a load from the controller.

        Returns:
            The value of the RGBW color as a tuple of (red, green, blue, white).
        """
        return tuple([await self.get_rgbw(vid, chan) for chan in self.RGBChannel])

    async def get_hsl_color(self, vid: int) -> tuple[int, ...]:
        """Get the HSL color of a load from the controller.

        Returns:
            The value of the HSL color as a tuple of (hue, saturation, lightness).
        """
        return tuple([await self.get_hsl(vid, attr) for attr in self.HSLAttribute])
