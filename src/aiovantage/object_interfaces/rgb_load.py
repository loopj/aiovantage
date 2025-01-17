"""Interface for querying and controlling RGB loads."""

from decimal import Decimal
from enum import IntEnum
from itertools import islice
from typing import NamedTuple

from .base import Interface, method


class RGBLoadInterface(Interface):
    """Interface for querying and controlling RGB loads."""

    # Types
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
        """The color names."""

        Unknown = 0
        White = 1
        Red = 2
        Yellow = 3
        Green = 4
        Magenta = 5
        Blue = 6
        Cyan = 7

    class ColorChannelResponse(NamedTuple):
        """A RGB(W) color channel response."""

        value: int
        channel: int

    # Properties
    rgb: tuple[int, int, int] | None = None  # RGBLoad.GetRGB
    rgbw: tuple[int, int, int, int] | None = None  # RGBLoad.GetRGBW
    hsl: tuple[int, int, int] | None = None  # RGBLoad.GetHSL
    color_name: ColorName | None = None

    # Methods
    @method("RGBLoad.SetRGB")
    async def set_rgb(self, red: int = 255, green: int = 255, blue: int = 255) -> None:
        """Set the color of an RGB load.

        Args:
            red: The red value of the color, (0-255)
            green: The green value of the color, (0-255)
            blue: The blue value of the color, (0-255)
        """
        # INVOKE <id> RGBLoad.SetRGB <red> <green> <blue>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGB <red> <green> <blue>
        await self.invoke("RGBLoad.SetRGB", red, green, blue)

    @method("RGBLoad.GetRGB")
    async def get_rgb(self, channel: RGBChannel) -> ColorChannelResponse:
        """Get a single RGB color channel of a load from the controller.

        Args:
            channel: The channel to get the color of.

        Returns:
            The value of the RGB channel, 0-255.
        """
        # INVOKE <id> RGBLoad.GetRGB <channel>
        # -> R:INVOKE <id> <value> RGBLoad.GetRGB <channel>
        return await self.invoke("RGBLoad.GetRGB", channel)

    @method("RGBLoad.SetRGBSW")
    async def set_rgb_sw(
        self, red: int = 255, green: int = 255, blue: int = 255
    ) -> None:
        """Set the cached color of an RGB load.

        Args:
            red: The red value of the color, (0-255)
            green: The green value of the color, (0-255)
            blue: The blue value of the color, (0-255)
        """
        # INVOKE <id> RGBLoad.SetRGBSW <red> <green> <blue>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGBSW <red> <green> <blue>
        await self.invoke("RGBLoad.SetRGBSW", red, green, blue)

    @method("RGBLoad.GetRGBHW")
    async def get_rgb_hw(self, channel: RGBChannel) -> ColorChannelResponse:
        """Get a single RGB color channel of a load directly from the hardware.

        Args:
            channel: The channel to get the color of.

        Returns:
            The value of the RGB channel, 0-255.
        """
        # INVOKE <id> RGBLoad.GetRGBHW <channel>
        # -> R:INVOKE <id> <value> RGBLoad.GetRGBHW <channel>
        return await self.invoke("RGBLoad.GetRGBHW", channel)

    @method("RGBLoad.SetHSL")
    async def set_hsl(
        self,
        hue: int,
        saturation: float | Decimal,
        lightness: float | Decimal,
    ) -> None:
        """Set the color of an HSL load.

        Args:
            hue: The hue value of the color, in degrees (0-360).
            saturation: The saturation value of the color, in percent (0-100).
            lightness: The lightness value of the color, in percent (0-100).
        """
        # INVOKE <id> RGBLoad.SetHSL <hue> <saturation> <lightness>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetHSL <hue> <saturation> <lightness>
        await self.invoke("RGBLoad.SetHSL", hue, saturation, lightness)

    @method("RGBLoad.GetHSL")
    async def get_hsl(self, attribute: HSLAttribute) -> ColorChannelResponse:
        """Get a single HSL color attribute of a load from the controller.

        Args:
            attribute: The attribute to get the value of.

        Returns:
            The value of the HSL attribute, 0-360 for hue, 0-100 for saturation and
            lightness.
        """
        # INVOKE <id> RGBLoad.GetHSL <attribute>
        # -> R:INVOKE <id> <value> RGBLoad.GetHSL <attribute>
        return await self.invoke("RGBLoad.GetHSL", attribute)

    @method("RGBLoad.SetHSLSW")
    async def set_hsl_sw(self, hue: int, saturation: int, lightness: int) -> None:
        """Set the cached color of an HSL load.

        Args:
            hue: The hue value of the color, in degrees (0-360).
            saturation: The saturation value of the color, in percent (0-100).
            lightness: The lightness value of the color, in percent (0-100).
        """
        # INVOKE <id> RGBLoad.SetHSLSW <hue> <saturation> <lightness>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetHSLSW <hue> <saturation> <lightness>
        await self.invoke("RGBLoad.SetHSLSW", hue, saturation, lightness)

    @method("RGBLoad.GetHSLHW")
    async def get_hsl_hw(self, attribute: HSLAttribute) -> ColorChannelResponse:
        """Get a single HSL color attribute of a load directly from the hardware.

        Args:
            attribute: The attribute to get the value of.

        Returns:
            The value of the HSL attribute, 0-360 for hue, 0-100 for saturation and
            lightness.
        """
        # INVOKE <id> RGBLoad.GetHSLHW <attribute>
        # -> R:INVOKE <id> <value> RGBLoad.GetHSLHW <attribute>
        return await self.invoke("RGBLoad.GetHSLHW", attribute)

    @method("RGBLoad.DissolveRGB")
    async def dissolve_rgb(
        self, red: int, green: int, blue: int, rate: float | Decimal
    ) -> None:
        """Transition the color of an RGB load over a number of seconds.

        Args:
            red: The new red value of the color, (0-255)
            green: The new green value of the color, (0-255)
            blue: The new blue value of the color, (0-255)
            rate: The number of seconds the transition should take.
        """
        # INVOKE <id> RGBLoad.DissolveRGB <red> <green> <blue> <rate>
        # -> R:INVOKE <id> <rcode> RGBLoad.DissolveRGB <red> <green> <blue> <rate>
        await self.invoke("RGBLoad.DissolveRGB", red, green, blue, rate)

    @method("RGBLoad.DissolveHSL")
    async def dissolve_hsl(
        self,
        hue: int,
        saturation: float | Decimal,
        lightness: float | Decimal,
        rate: float | Decimal,
    ) -> None:
        """Transition the color of an HSL load over a number of seconds.

        Args:
            hue: The new hue value of the color, in degrees (0-360).
            saturation: The new saturation value of the color, in percent (0-100).
            lightness: The new lightness value of the color, in percent (0-100).
            rate: The number of seconds the transition should take.
        """
        # INVOKE <id> RGBLoad.DissolveHSL <hue> <saturation> <lightness> <rate>
        # -> R:INVOKE <id> <rcode> RGBLoad.DissolveHSL <hue> <saturation> <lightness> <rate>
        await self.invoke("RGBLoad.DissolveHSL", hue, saturation, lightness, rate)

    @method("RGBLoad.SetDissolveRate")
    async def set_dissolve_rate(self, rate: float | Decimal) -> None:
        """Set the default dissolve rate for RGB and HSL transitions.

        Args:
            rate: The number of seconds the transition should take.
        """
        # INVOKE <id> RGBLoad.SetDissolveRate <rate>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetDissolveRate <rate>
        await self.invoke("RGBLoad.SetDissolveRate", rate)

    @method("RGBLoad.GetDissolveRate")
    async def get_dissolve_rate(self) -> Decimal:
        """Get the default dissolve rate for RGB and HSL transitions.

        Returns:
            The number of seconds the transition should take.
        """
        # INVOKE <id> RGBLoad.GetDissolveRate
        # -> R:INVOKE <id> <rate> RGBLoad.GetDissolveRate
        return await self.invoke("RGBLoad.GetDissolveRate")

    @method("RGBLoad.SetDissolveRateSW")
    async def set_dissolve_rate_sw(self, rate: float | Decimal) -> None:
        """Set the cached default dissolve rate for RGB and HSL transitions.

        Args:
            rate: The number of seconds the transition should take.
        """
        # INVOKE <id> RGBLoad.SetDissolveRateSW <rate>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetDissolveRateSW <rate>
        await self.invoke("RGBLoad.SetDissolveRateSW", rate)

    @method("RGBLoad.GetDissolveRateHW")
    async def get_dissolve_rate_hw(self) -> Decimal:
        """Get the default dissolve rate for RGB and HSL transitions directly from the hardware.

        Returns:
            The number of seconds the transition should take.
        """
        # INVOKE <id> RGBLoad.GetDissolveRateHW
        # -> R:INVOKE <id> <rate> RGBLoad.GetDissolveRateHW
        return await self.invoke("RGBLoad.GetDissolveRateHW")

    @method("RGBLoad.IncrementRGBComponent")
    async def increment_rgb_component(self, channel: RGBChannel) -> None:
        """Increment a single RGB color channel of a load.

        Args:
            channel: The channel to increment the color of.
        """
        # INVOKE <id> RGBLoad.IncrementRGBComponent <channel>
        # -> R:INVOKE <id> <rcode> RGBLoad.IncrementRGBComponent <channel>
        await self.invoke("RGBLoad.IncrementRGBComponent", channel)

    @method("RGBLoad.DecrementRGBComponent")
    async def decrement_rgb_component(self, channel: RGBChannel) -> None:
        """Decrement a single RGB color channel of a load.

        Args:
            channel: The channel to decrement the color of.
        """
        # INVOKE <id> RGBLoad.DecrementRGBComponent <channel>
        # -> R:INVOKE <id> <rcode> RGBLoad.DecrementRGBComponent <channel>
        await self.invoke("RGBLoad.DecrementRGBComponent", channel)

    @method("RGBLoad.SetRGBComponent")
    async def set_rgb_component(self, channel: RGBChannel, value: int) -> None:
        """Set a single RGB(W) color channel of a load.

        Args:
            channel: The channel to set the color of.
            value: The value to set the channel to, 0-255.
        """
        # INVOKE <id> RGBLoad.SetRGBComponent <channel> <value>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGBComponent <channel> <value>
        await self.invoke("RGBLoad.SetRGBComponent", channel, value)

    @method("RGBLoad.IncrementHSLAttribute")
    async def increment_hsl_attribute(self, attribute: HSLAttribute) -> None:
        """Increment a single HSL color attribute of a load.

        Args:
            attribute: The attribute to increment the value of.
        """
        # INVOKE <id> RGBLoad.IncrementHSLAttribute <attribute>
        # -> R:INVOKE <id> <rcode> RGBLoad.IncrementHSLAttribute <attribute>
        await self.invoke("RGBLoad.IncrementHSLAttribute", attribute)

    @method("RGBLoad.DecrementHSLAttribute")
    async def decrement_hsl_attribute(self, attribute: HSLAttribute) -> None:
        """Decrement a single HSL color attribute of a load.

        Args:
            attribute: The attribute to decrement the value of.
        """
        # INVOKE <id> RGBLoad.DecrementHSLAttribute <attribute>
        # -> R:INVOKE <id> <rcode> RGBLoad.DecrementHSLAttribute <attribute>
        await self.invoke("RGBLoad.DecrementHSLAttribute", attribute)

    @method("RGBLoad.SetHSLAttribute")
    async def set_hsl_attribute(self, attribute: HSLAttribute, value: int) -> None:
        """Set a single HSL color attribute of a load.

        Args:
            attribute: The attribute to set the value of.
            value: The value to set the attribute to, 0-360 for hue, 0-100 for
                saturation and lightness.
        """
        # INVOKE <id> RGBLoad.SetHSLAttribute <attribute> <value>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetHSLAttribute <attribute> <value>
        await self.invoke("RGBLoad.SetHSLAttribute", attribute, value)

    @method("RGBLoad.Stop")
    async def stop(self) -> None:
        """Stop the transition."""
        # INVOKE <id> RGBLoad.Stop
        # -> R:INVOKE <id> <rcode> RGBLoad.Stop
        await self.invoke("RGBLoad.Stop")

    @method("RGBLoad.NextPreset")
    async def next_preset(self) -> None:
        """Change to the next lighting preset."""
        # INVOKE <id> RGBLoad.NextPreset
        # -> R:INVOKE <id> <rcode> RGBLoad.NextPreset
        await self.invoke("RGBLoad.NextPreset")

    @method("RGBLoad.PreviousPreset")
    async def previous_preset(self) -> None:
        """Change to the previous lighting preset."""
        # INVOKE <id> RGBLoad.PreviousPreset
        # -> R:INVOKE <id> <rcode> RGBLoad.PreviousPreset
        await self.invoke("RGBLoad.PreviousPreset")

    @method("RGBLoad.NextEffect")
    async def next_effect(self) -> None:
        """Change to the next lighting effect."""
        # INVOKE <id> RGBLoad.NextEffect
        # -> R:INVOKE <id> <rcode> RGBLoad.NextEffect
        await self.invoke("RGBLoad.NextEffect")

    @method("RGBLoad.PreviousEffect")
    async def previous_effect(self) -> None:
        """Change to the previous lighting effect."""
        # INVOKE <id> RGBLoad.PreviousEffect
        # -> R:INVOKE <id> <rcode> RGBLoad.PreviousEffect
        await self.invoke("RGBLoad.PreviousEffect")

    @method("RGBLoad.SetPreset")
    async def set_preset(self, index: int) -> None:
        """Change to a specific lighting preset.

        Args:
            index: The index of the preset to change to.
        """
        # INVOKE <id> RGBLoad.SetPreset <index>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetPreset <index>
        await self.invoke("RGBLoad.SetPreset", index)

    @method("RGBLoad.GetPreset")
    async def get_preset(self) -> int:
        """Get the current lighting preset.

        Returns:
            The index of the current preset.
        """
        # INVOKE <id> RGBLoad.GetPreset
        # -> R:INVOKE <id> <index> RGBLoad.GetPreset
        return await self.invoke("RGBLoad.GetPreset")

    @method("RGBLoad.SetPresetSW")
    async def set_preset_sw(self, index: int) -> None:
        """Set the cached lighting preset.

        Args:
            index: The index of the preset to change to.
        """
        # INVOKE <id> RGBLoad.SetPresetSW <index>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetPresetSW <index>
        await self.invoke("RGBLoad.SetPresetSW", index)

    @method("RGBLoad.GetPresetHW")
    async def get_preset_hw(self) -> int:
        """Get the current lighting preset directly from the hardware.

        Returns:
            The index of the current preset.
        """
        # INVOKE <id> RGBLoad.GetPresetHW
        # -> R:INVOKE <id> <index> RGBLoad.GetPresetHW
        return await self.invoke("RGBLoad.GetPresetHW")

    @method("RGBLoad.SetEffect")
    async def set_effect(self, index: int) -> None:
        """Change to a specific lighting effect.

        Args:
            index: The index of the effect to change to.
        """
        # INVOKE <id> RGBLoad.SetEffect <index>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetEffect <index>
        await self.invoke("RGBLoad.SetEffect", index)

    @method("RGBLoad.GetEffect")
    async def get_effect(self) -> int:
        """Get the current lighting effect.

        Returns:
            The index of the current effect.
        """
        # INVOKE <id> RGBLoad.GetEffect
        # -> R:INVOKE <id> <index> RGBLoad.GetEffect
        return await self.invoke("RGBLoad.GetEffect")

    @method("RGBLoad.SetEffectSW")
    async def set_effect_sw(self, index: int) -> None:
        """Set the cached lighting effect.

        Args:
            index: The index of the effect to change to.
        """
        # INVOKE <id> RGBLoad.SetEffectSW <index>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetEffectSW <index>
        await self.invoke("RGBLoad.SetEffectSW", index)

    @method("RGBLoad.GetEffectHW")
    async def get_effect_hw(self) -> int:
        """Get the current lighting effect directly from the hardware.

        Returns:
            The index of the current effect.
        """
        # INVOKE <id> RGBLoad.GetEffectHW
        # -> R:INVOKE <id> <index> RGBLoad.GetEffectHW
        return await self.invoke("RGBLoad.GetEffectHW")

    @method("RGBLoad.SetColorByName")
    async def set_color_by_name(self, color: ColorName) -> None:
        """Set the color of an RGB load by name.

        Args:
            color: The name of the color to set the load to.
        """
        # INVOKE <id> RGBLoad.SetColorByName <color>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetColorByName <color>
        await self.invoke("RGBLoad.SetColorByName", color)

    @method("RGBLoad.GetColorName", property="color_name")
    async def get_color_name(self) -> ColorName:
        """Get the name of the color of a load from the controller.

        Returns:
            The name of the color.
        """
        # INVOKE <id> RGBLoad.GetColorName
        # -> R:INVOKE <id> <color> RGBLoad.GetColorName
        return await self.invoke("RGBLoad.GetColorName")

    @method("RGBLoad.GetColor")
    async def get_color(self) -> int:
        """Get the RGB/RGBW color of a load from the controller.

        Returns:
            The RGB(W) value of the color as a packed big-endian integer.
        """
        # To unpack the response:
        # response.to_bytes(4, byteorder='big', signed=True)
        # NOTE: The W value always seems to be 0, even for RGBW loads.

        # INVOKE <id> RGBLoad.GetColor
        # -> R:INVOKE <id> <color> RGBLoad.GetColor
        return await self.invoke("RGBLoad.GetColor")

    @method("RGBLoad.GetColorHW")
    async def get_color_hw(self) -> int:
        """Get the RGB/RGBW color of a load directly from the hardware.

        Returns:
            The RGB(W) value of the color as a packed big-endian integer.
        """
        # INVOKE <id> RGBLoad.GetColorHW
        # -> R:INVOKE <id> <color> RGBLoad.GetColorHW
        return await self.invoke("RGBLoad.GetColorHW")

    @method("RGBLoad.SetRGBW")
    async def set_rgbw(
        self, red: int = 255, green: int = 255, blue: int = 255, white: int = 255
    ) -> None:
        """Set the color of an RGBW load.

        Args:
            red: The red value of the color, (0-255)
            green: The green value of the color, (0-255)
            blue: The blue value of the color, (0-255)
            white: The white value of the color, (0-255)
        """
        # INVOKE <id> RGBLoad.SetRGBW <red> <green> <blue> <white>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGBW <red> <green> <blue> <white>
        await self.invoke("RGBLoad.SetRGBW", red, green, blue, white)

    @method("RGBLoad.GetRGBW")
    async def get_rgbw(self, channel: int) -> ColorChannelResponse:
        """Get a single RGBW color channel of a load from the controller.

        Args:
            channel: The channel to get the color of.

        Returns:
            The value of the RGBW channel, 0-255.
        """
        # INVOKE <id> RGBLoad.GetRGBW <channel>
        # -> R:INVOKE <id> <value> RGBLoad.GetRGBW <channel>
        return await self.invoke("RGBLoad.GetRGBW", channel)

    @method("RGBLoad.SetRGBWSW")
    async def set_rgbw_sw(
        self, red: int = 255, green: int = 255, blue: int = 255, white: int = 255
    ) -> None:
        """Set the cached color of an RGBW load.

        Args:
            red: The red value of the color, (0-255)
            green: The green value of the color, (0-255)
            blue: The blue value of the color, (0-255)
            white: The white value of the color, (0-255)
        """
        # INVOKE <id> RGBLoad.SetRGBWSW <red> <green> <blue> <white>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGBWSW <red> <green> <blue> <white>
        await self.invoke("RGBLoad.SetRGBWSW", red, green, blue, white)

    @method("RGBLoad.GetRGBWHW")
    async def get_rgbw_hw(self, channel: int) -> int:
        """Get a single RGBW color channel of a load directly from the hardware.

        Args:
            channel: The channel to get the color of.

        Returns:
            The value of the RGBW channel, 0-255.
        """
        # INVOKE <id> RGBLoad.GetRGBWHW <channel>
        # -> R:INVOKE <id> <value> RGBLoad.GetRGBWHW <channel>
        return await self.invoke("RGBLoad.GetRGBWHW", channel)

    @method("RGBLoad.GetTransitionLevel")
    async def get_transition_level(self) -> Decimal:
        """Get the transition level of a load.

        Returns:
            The transition level of the load.
        """
        # INVOKE <id> RGBLoad.GetTransitionLevel
        # -> R:INVOKE <id> <level> RGBLoad.GetTransitionLevel
        return await self.invoke("RGBLoad.GetTransitionLevel")

    # Additional convenience methods, not part of the Vantage API
    async def get_rgb_color(self) -> tuple[int, ...]:
        """Get the RGB color of a load from the controller.

        Returns:
            The value of the RGB color as a tuple of (red, green, blue).
        """
        rgb: list[int] = []
        for chan in islice(self.RGBChannel, 3):
            result = await self.get_rgb(chan)
            rgb.append(result.value)

        return tuple(rgb)

    async def get_rgbw_color(self) -> tuple[int, ...]:
        """Get the RGBW color of a load from the controller.

        Returns:
            The value of the RGBW color as a tuple of (red, green, blue, white).
        """
        rgbw: list[int] = []
        for chan in self.RGBChannel:
            result = await self.get_rgbw(chan)
            rgbw.append(result.value)

        return tuple(rgbw)

    async def get_hsl_color(self) -> tuple[int, ...]:
        """Get the HSL color of a load from the controller.

        Returns:
            The value of the HSL color as a tuple of (hue, saturation, lightness).
        """
        hsl: list[int] = []
        for attr in self.HSLAttribute:
            result = await self.get_hsl(attr)
            hsl.append(result.value)

        return tuple(hsl)
