from decimal import Decimal
from enum import IntEnum
from itertools import islice

from typing_extensions import override

from aiovantage.command_client import Converter
from aiovantage.errors import CommandError

from .base import Interface, method


class RGBLoadInterface(Interface):
    """RGB load interface."""

    interface_name = "RGBLoad"

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

    # Properties
    rgb: tuple[int, int, int] | None = None
    rgbw: tuple[int, int, int, int] | None = None
    hsl: tuple[int, int, int] | None = None

    # Methods
    @method("SetRGB", "SetRGBSW", "SetRGBFollowLevel")
    async def set_rgb(
        self,
        red: int = 255,
        green: int = 255,
        blue: int = 255,
        *,
        sw: bool = False,
        follow_level: bool = False,
    ) -> None:
        """Set the color of an RGB load.

        Args:
            red: The red value of the color, (0-255)
            green: The green value of the color, (0-255)
            blue: The blue value of the color, (0-255)
            sw: Set the cached value instead of the hardware value.
            follow_level: Follow the level of the load.
        """
        # INVOKE <id> RGBLoad.SetRGB <red> <green> <blue>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGB <red> <green> <blue>
        if follow_level and sw:
            raise ValueError("Cannot set both follow_level and sw")

        if follow_level:
            method = "RGBLoad.SetRGBFollowLevel"
        elif sw:
            method = "RGBLoad.SetRGBSW"
        else:
            method = "RGBLoad.SetRGB"

        await self.invoke(method, red, green, blue)

    @method("GetRGB", "GetRGBHW")
    async def get_rgb(self, channel: RGBChannel, *, hw: bool = False) -> int:
        """Get a single RGB color channel of a load from the controller.

        Args:
            channel: The channel to get the color of.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The value of the RGB channel, 0-255.
        """
        # INVOKE <id> RGBLoad.GetRGB <channel>
        # -> R:INVOKE <id> <value> RGBLoad.GetRGB <channel>
        return await self.invoke(
            "RGBLoad.GetRGBHW" if hw else "RGBLoad.GetRGB", channel
        )

    @method("SetHSL", "SetHSLSW")
    async def set_hsl(
        self,
        hue: int,
        saturation: float | Decimal,
        lightness: float | Decimal,
        *,
        sw: bool = False,
    ) -> None:
        """Set the color of an HSL load.

        Args:
            hue: The hue value of the color, in degrees (0-360).
            saturation: The saturation value of the color, in percent (0-100).
            lightness: The lightness value of the color, in percent (0-100).
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> RGBLoad.SetHSL <hue> <saturation> <lightness>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetHSL <hue> <saturation> <lightness>
        await self.invoke(
            "RGBLoad.SetHSLSW" if sw else "RGBLoad.SetHSL", hue, saturation, lightness
        )

    @method("GetHSL", "GetHSLHW")
    async def get_hsl(self, attribute: HSLAttribute, *, hw: bool = False) -> int:
        """Get a single HSL color attribute of a load from the controller.

        Args:
            attribute: The attribute to get the value of.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The value of the HSL attribute, 0-360 for hue, 0-100 for saturation and
            lightness.
        """
        # INVOKE <id> RGBLoad.GetHSL <attribute>
        # -> R:INVOKE <id> <value> RGBLoad.GetHSL <attribute>
        return await self.invoke(
            "RGBLoad.GetHSLHW" if hw else "RGBLoad.GetHSL", attribute
        )

    @method("DissolveRGB", "DissolveRGBFollowLevel")
    async def dissolve_rgb(
        self,
        red: int,
        green: int,
        blue: int,
        rate: float | Decimal,
        *,
        follow_level: bool = False,
    ) -> None:
        """Transition the color of an RGB load over a number of seconds.

        Args:
            red: The new red value of the color, (0-255)
            green: The new green value of the color, (0-255)
            blue: The new blue value of the color, (0-255)
            rate: The number of seconds the transition should take.
            follow_level: Follow the level of the load.
        """
        # INVOKE <id> RGBLoad.DissolveRGB <red> <green> <blue> <rate>
        # -> R:INVOKE <id> <rcode> RGBLoad.DissolveRGB <red> <green> <blue> <rate>
        if follow_level:
            method = "RGBLoad.DissolveRGBFollowLevel"
        else:
            method = "RGBLoad.DissolveRGB"

        await self.invoke(method, red, green, blue, rate)

    @method("DissolveHSL")
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

    @method("SetDissolveRate", "SetDissolveRateSW")
    async def set_dissolve_rate(
        self, rate: float | Decimal, *, sw: bool = False
    ) -> None:
        """Set the default dissolve rate for RGB and HSL transitions.

        Args:
            rate: The number of seconds the transition should take.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> RGBLoad.SetDissolveRate <rate>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetDissolveRate <rate>
        await self.invoke(
            "RGBLoad.SetDissolveRateSW" if sw else "RGBLoad.SetDissolveRate", rate
        )

    @method("GetDissolveRate", "GetDissolveRateHW")
    async def get_dissolve_rate(self, *, hw: bool = False) -> Decimal:
        """Get the default dissolve rate for RGB and HSL transitions.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The number of seconds the transition should take.
        """
        # INVOKE <id> RGBLoad.GetDissolveRate
        # -> R:INVOKE <id> <rate> RGBLoad.GetDissolveRate
        return await self.invoke(
            "RGBLoad.GetDissolveRateHW" if hw else "RGBLoad.GetDissolveRate"
        )

    @method("IncrementRGBComponent")
    async def increment_rgb_component(self, channel: RGBChannel) -> None:
        """Increment a single RGB color channel of a load.

        Args:
            channel: The channel to increment the color of.
        """
        # INVOKE <id> RGBLoad.IncrementRGBComponent <channel>
        # -> R:INVOKE <id> <rcode> RGBLoad.IncrementRGBComponent <channel>
        await self.invoke("RGBLoad.IncrementRGBComponent", channel)

    @method("DecrementRGBComponent")
    async def decrement_rgb_component(self, channel: RGBChannel) -> None:
        """Decrement a single RGB color channel of a load.

        Args:
            channel: The channel to decrement the color of.
        """
        # INVOKE <id> RGBLoad.DecrementRGBComponent <channel>
        # -> R:INVOKE <id> <rcode> RGBLoad.DecrementRGBComponent <channel>
        await self.invoke("RGBLoad.DecrementRGBComponent", channel)

    @method("SetRGBComponent")
    async def set_rgb_component(self, channel: RGBChannel, value: int) -> None:
        """Set a single RGB(W) color channel of a load.

        Args:
            channel: The channel to set the color of.
            value: The value to set the channel to, 0-255.
        """
        # INVOKE <id> RGBLoad.SetRGBComponent <channel> <value>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGBComponent <channel> <value>
        await self.invoke("RGBLoad.SetRGBComponent", channel, value)

    @method("IncrementHSLAttribute")
    async def increment_hsl_attribute(self, attribute: HSLAttribute) -> None:
        """Increment a single HSL color attribute of a load.

        Args:
            attribute: The attribute to increment the value of.
        """
        # INVOKE <id> RGBLoad.IncrementHSLAttribute <attribute>
        # -> R:INVOKE <id> <rcode> RGBLoad.IncrementHSLAttribute <attribute>
        await self.invoke("RGBLoad.IncrementHSLAttribute", attribute)

    @method("DecrementHSLAttribute")
    async def decrement_hsl_attribute(self, attribute: HSLAttribute) -> None:
        """Decrement a single HSL color attribute of a load.

        Args:
            attribute: The attribute to decrement the value of.
        """
        # INVOKE <id> RGBLoad.DecrementHSLAttribute <attribute>
        # -> R:INVOKE <id> <rcode> RGBLoad.DecrementHSLAttribute <attribute>
        await self.invoke("RGBLoad.DecrementHSLAttribute", attribute)

    @method("SetHSLAttribute")
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

    @method("Stop")
    async def stop(self) -> None:
        """Stop the transition."""
        # INVOKE <id> RGBLoad.Stop
        # -> R:INVOKE <id> <rcode> RGBLoad.Stop
        await self.invoke("RGBLoad.Stop")

    @method("NextPreset")
    async def next_preset(self) -> None:
        """Change to the next lighting preset."""
        # INVOKE <id> RGBLoad.NextPreset
        # -> R:INVOKE <id> <rcode> RGBLoad.NextPreset
        await self.invoke("RGBLoad.NextPreset")

    @method("PreviousPreset")
    async def previous_preset(self) -> None:
        """Change to the previous lighting preset."""
        # INVOKE <id> RGBLoad.PreviousPreset
        # -> R:INVOKE <id> <rcode> RGBLoad.PreviousPreset
        await self.invoke("RGBLoad.PreviousPreset")

    @method("NextEffect")
    async def next_effect(self) -> None:
        """Change to the next lighting effect."""
        # INVOKE <id> RGBLoad.NextEffect
        # -> R:INVOKE <id> <rcode> RGBLoad.NextEffect
        await self.invoke("RGBLoad.NextEffect")

    @method("PreviousEffect")
    async def previous_effect(self) -> None:
        """Change to the previous lighting effect."""
        # INVOKE <id> RGBLoad.PreviousEffect
        # -> R:INVOKE <id> <rcode> RGBLoad.PreviousEffect
        await self.invoke("RGBLoad.PreviousEffect")

    @method("SetPreset", "SetPresetSW")
    async def set_preset(self, index: int, *, sw: bool = False) -> None:
        """Change to a specific lighting preset.

        Args:
            index: The index of the preset to change to.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> RGBLoad.SetPreset <index>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetPreset <index>
        await self.invoke("RGBLoad.SetPresetSW" if sw else "RGBLoad.SetPreset", index)

    @method("GetPreset", "GetPresetHW")
    async def get_preset(self, *, hw: bool = False) -> int:
        """Get the current lighting preset.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The index of the current preset.
        """
        # INVOKE <id> RGBLoad.GetPreset
        # -> R:INVOKE <id> <index> RGBLoad.GetPreset
        return await self.invoke("RGBLoad.GetPresetHW" if hw else "RGBLoad.GetPreset")

    @method("SetEffect", "SetEffectSW")
    async def set_effect(self, index: int, *, sw: bool = False) -> None:
        """Change to a specific lighting effect.

        Args:
            index: The index of the effect to change to.
            sw: Set the cached value instead of the hardware value.
        """
        # INVOKE <id> RGBLoad.SetEffect <index>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetEffect <index>
        await self.invoke("RGBLoad.SetEffectSW" if sw else "RGBLoad.SetEffect", index)

    @method("GetEffect", "GetEffectHW")
    async def get_effect(self, *, hw: bool = False) -> int:
        """Get the current lighting effect.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The index of the current effect.
        """
        # INVOKE <id> RGBLoad.GetEffect
        # -> R:INVOKE <id> <index> RGBLoad.GetEffect
        return await self.invoke("RGBLoad.GetEffectHW" if hw else "RGBLoad.GetEffect")

    @method("SetColorByName")
    async def set_color_by_name(self, color: ColorName) -> None:
        """Set the color of an RGB load by name.

        Args:
            color: The name of the color to set the load to.
        """
        # INVOKE <id> RGBLoad.SetColorByName <color>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetColorByName <color>
        await self.invoke("RGBLoad.SetColorByName", color)

    @method("GetColorName")
    async def get_color_name(self) -> ColorName:
        """Get the name of the color of a load from the controller.

        Returns:
            The name of the color.
        """
        # INVOKE <id> RGBLoad.GetColorName
        # -> R:INVOKE <id> <color> RGBLoad.GetColorName
        return await self.invoke("RGBLoad.GetColorName")

    @method("GetColor", "GetColorHW")
    async def get_color(self, *, hw: bool = False) -> int:
        """Get the RGB/RGBW color of a load from the controller.

        Args:
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The RGB(W) value of the color as a packed big-endian integer.
        """
        # To unpack the response:
        # response.to_bytes(4, byteorder='big', signed=True)
        # NOTE: The W value always seems to be 0, even for RGBW loads.

        # INVOKE <id> RGBLoad.GetColor
        # -> R:INVOKE <id> <color> RGBLoad.GetColor
        return await self.invoke("RGBLoad.GetColorHW" if hw else "RGBLoad.GetColor")

    @method("SetRGBW", "SetRGBWSW", "SetRGBWFollowLevel")
    async def set_rgbw(
        self,
        red: int = 255,
        green: int = 255,
        blue: int = 255,
        white: int = 255,
        *,
        sw: bool = False,
        follow_level: bool = False,
    ) -> None:
        """Set the color of an RGBW load.

        Args:
            red: The red value of the color, (0-255)
            green: The green value of the color, (0-255)
            blue: The blue value of the color, (0-255)
            white: The white value of the color, (0-255)
            sw: Set the cached value instead of the hardware value.
            follow_level: Follow the level of the load.
        """
        # INVOKE <id> RGBLoad.SetRGBW <red> <green> <blue> <white>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGBW <red> <green> <blue> <white>
        if follow_level and sw:
            raise ValueError("Cannot set both follow_level and sw")

        if follow_level:
            method = "RGBLoad.SetRGBWFollowLevel"
        elif sw:
            method = "RGBLoad.SetRGBWSW"
        else:
            method = "RGBLoad.SetRGBW"

        await self.invoke(method, red, green, blue, white)

    @method("GetRGBW", "GetRGBWHW")
    async def get_rgbw(self, channel: int, *, hw: bool = False) -> int:
        """Get a single RGBW color channel of a load from the controller.

        Args:
            channel: The channel to get the color of.
            hw: Fetch the value from hardware instead of cache.

        Returns:
            The value of the RGBW channel, 0-255.
        """
        # INVOKE <id> RGBLoad.GetRGBW <channel>
        # -> R:INVOKE <id> <value> RGBLoad.GetRGBW <channel>
        return await self.invoke(
            "RGBLoad.GetRGBWHW" if hw else "RGBLoad.GetRGBW", channel
        )

    @method("GetTransitionLevel")
    async def get_transition_level(self) -> Decimal:
        """Get the transition level of a load.

        Returns:
            The transition level of the load.
        """
        # INVOKE <id> RGBLoad.GetTransitionLevel
        # -> R:INVOKE <id> <level> RGBLoad.GetTransitionLevel
        return await self.invoke("RGBLoad.GetTransitionLevel")

    @method("DissolveRGBW", "DissolveRGBWFollowLevel")
    async def dissolve_rgbw(
        self,
        red: int,
        green: int,
        blue: int,
        white: int,
        rate: float | Decimal,
        *,
        follow_level: bool = False,
    ) -> None:
        """Transition the color of an RGBW load over a number of seconds.

        Args:
            red: The new red value of the color, (0-255)
            green: The new green value of the color, (0-255)
            blue: The new blue value of the color, (0-255)
            white: The new white value of the color, (0-255)
            rate: The number of seconds the transition should take.
            follow_level: Follow the level of the load.
        """
        # INVOKE <id> RGBLoad.DissolveRGBW <red> <green> <blue> <white> <rate>
        # -> R:INVOKE <id> <rcode> RGBLoad.DissolveRGBW <red> <green> <blue> <white> <rate>
        if follow_level:
            method = "RGBLoad.DissolveRGBWFollowLevel"
        else:
            method = "RGBLoad.DissolveRGBW"

        await self.invoke(method, red, green, blue, white, rate)

    # Convenience functions, not part of the interface
    async def get_rgb_color(self) -> tuple[int, int, int]:
        """Get the RGB color of a load from the controller.

        Returns:
            The value of the RGB color as a tuple of (red, green, blue).
        """
        return tuple[int, int, int](
            [await self.get_rgb(chan) for chan in islice(self.RGBChannel, 3)]
        )

    async def get_rgbw_color(self) -> tuple[int, int, int, int]:
        """Get the RGBW color of a load from the controller.

        Returns:
            The value of the RGBW color as a tuple of (red, green, blue, white).
        """
        return tuple[int, int, int, int](
            [await self.get_rgbw(chan) for chan in self.RGBChannel]
        )

    async def get_hsl_color(self) -> tuple[int, int, int]:
        """Get the HSL color of a load from the controller.

        Returns:
            The value of the HSL color as a tuple of (hue, saturation, lightness).
        """
        return tuple[int, int, int](
            [await self.get_hsl(attr) for attr in self.HSLAttribute]
        )

    # The rgb, hsl, and rgbw properties are "virtual" properties that are populated
    # by fetching the individual color channels/attributes.
    # For status updates, we need to wait for all channels/attributes to be received
    # before updating the property.

    @override
    async def fetch_state(self) -> list[str]:
        # Fetch state from other interfaces first
        props_changed = await super().fetch_state()

        # Define the getters for our "virtual" properties
        getters = {
            "rgb": self.get_rgb_color,
            "hsl": self.get_hsl_color,
            "rgbw": self.get_rgbw_color,
        }

        # Fetch the properties
        for prop, getter in getters.items():
            try:
                props_changed.extend(self.update_properties({prop: await getter()}))
            except CommandError:
                continue

        return props_changed

    @override
    def handle_object_status(self, method: str, result: str, *args: str) -> list[str]:
        # Define the methods and the number of channels/attributes they return
        methods = {
            "RGBLoad.GetRGB": ("rgb", 3),
            "RGBLoad.GetHSL": ("hsl", 3),
            "RGBLoad.GetRGBW": ("rgbw", 4),
        }

        # Check if the method is one we're interested in
        if method not in methods:
            return super().handle_object_status(method, result, *args)

        # Get the attribute and number of channels/attributes
        attr, num_channels = methods[method]

        # Ignore channels that are out of range
        channel = Converter.deserialize(int, args[0])
        if channel not in range(num_channels):
            return []

        # Cache the value
        self._cache = getattr(self, "_cache", [0, 0, 0, 0])
        self._cache[channel] = Converter.deserialize(int, result)

        # Update the property only if all channels have been received
        if channel == num_channels - 1:
            new_value = tuple(self._cache[:num_channels])
            return self.update_properties({attr: new_value})

        return []
