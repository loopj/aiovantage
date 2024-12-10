"""Interface for querying and controlling RGB loads."""

from decimal import Decimal
from enum import IntEnum
from typing import NamedTuple

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

    class ColorChannelResponse(NamedTuple):
        """A RGB(W) color channel response."""

        value: int
        channel: int

    method_signatures = {
        "RGBLoad.GetRGB": ColorChannelResponse,
        "RGBLoad.GetRGBW": ColorChannelResponse,
        "RGBLoad.GetHSL": ColorChannelResponse,
        "RGBLoad.GetColor": int,
    }

    hsl: tuple[int, int, int]
    rgb: tuple[int, int, int]
    rgbw: tuple[int, int, int, int]

    async def set_rgb(self, red: int, green: int, blue: int) -> None:
        """Set the color of an RGB load.

        Args:
            red: The red value of the color, (0-255)
            green: The green value of the color, (0-255)
            blue: The blue value of the color, (0-255)
        """
        # Clamp levels to 0-255
        red = max(min(red, 255), 0)
        green = max(min(green, 255), 0)
        blue = max(min(blue, 255), 0)

        # INVOKE <id> RGBLoad.SetRGB <red> <green> <blue>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGB <red> <green> <blue>
        await self.invoke("RGBLoad.SetRGB", red, green, blue)

    async def get_rgb(self, channel: int) -> int:
        """Get a single RGB color channel of a load from the controller.

        Args:
            channel: The channel to get the color of.

        Returns:
            The value of the RGB channel, 0-255.
        """
        # INVOKE <id> RGBLoad.GetRGB <channel>
        # -> R:INVOKE <id> <value> RGBLoad.GetRGB <channel>
        response = await RGBLoadInterface.invoke(
            self, "RGBLoad.GetRGB", channel, as_type=self.ColorChannelResponse
        )
        return response.value

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
        # Clamp levels to 0-360, 0-100
        hue = max(min(hue, 360), 0)
        saturation = max(min(saturation, 100), 0)
        lightness = max(min(lightness, 100), 0)

        # INVOKE <id> RGBLoad.SetHSL <hue> <saturation> <lightness>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetHSL <hue> <saturation> <lightness>
        await self.invoke("RGBLoad.SetHSL", hue, saturation, lightness)

    async def get_hsl(self, attribute: int) -> int:
        """Get a single HSL color attribute of a load from the controller.

        Args:
            attribute: The attribute to get the value of.

        Returns:
            The value of the HSL attribute, 0-360 for hue, 0-100 for saturation and
            lightness.
        """
        # INVOKE <id> RGBLoad.GetHSL <attribute>
        # -> R:INVOKE <id> <value> RGBLoad.GetHSL <attribute>
        response = await RGBLoadInterface.invoke(
            self, "RGBLoad.GetHSL", attribute, as_type=self.ColorChannelResponse
        )
        return response.value

    async def dissolve_rgb(
        self, red: float, green: float, blue: float, rate: float
    ) -> None:
        """Transition the color of an RGB load over a number of seconds.

        Args:
            red: The new red value of the color, (0-255)
            green: The new green value of the color, (0-255)
            blue: The new blue value of the color, (0-255)
            rate: The number of seconds the transition should take.
        """
        # Clamp levels to 0-255, ensure they're integers
        red = int(max(min(red, 255), 0))
        green = int(max(min(green, 255), 0))
        blue = int(max(min(blue, 255), 0))

        # INVOKE <id> RGBLoad.DissolveRGB <red> <green> <blue> <rate>
        # -> R:INVOKE <id> <rcode> RGBLoad.DissolveRGB <red> <green> <blue> <rate>
        await self.invoke("RGBLoad.DissolveRGB", red, green, blue, rate)

    async def dissolve_hsl(
        self, hue: float, saturation: float, lightness: float, rate: float
    ) -> None:
        """Transition the color of an HSL load over a number of seconds.

        Args:
            hue: The new hue value of the color, in degrees (0-360).
            saturation: The new saturation value of the color, in percent (0-100).
            lightness: The new lightness value of the color, in percent (0-100).
            rate: The number of seconds the transition should take.
        """
        # Clamp levels to 0-360, 0-100, ensure they're integers
        hue = int(max(min(hue, 360), 0))
        saturation = int(max(min(saturation, 100), 0))
        lightness = int(max(min(lightness, 100), 0))

        # INVOKE <id> RGBLoad.DissolveHSL <hue> <saturation> <lightness> <rate>
        # -> R:INVOKE <id> <rcode> RGBLoad.DissolveHSL <hue> <saturation> <lightness> <rate>
        await self.invoke("RGBLoad.DissolveHSL", hue, saturation, lightness, rate)

    async def set_rgb_component(self, channel: RGBChannel, value: int) -> None:
        """Set a single RGB(W) color channel of a load.

        Args:
            channel: The channel to set the color of.
            value: The value to set the channel to, 0-255.
        """
        # Clamp value to 0-255
        value = max(min(value, 255), 0)

        # INVOKE <id> RGBLoad.SetRGBComponent <channel> <value>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGBComponent <channel> <value>
        await self.invoke("RGBLoad.SetRGBComponent", channel, value)

    async def set_hsl_attribute(self, attribute: HSLAttribute, value: int) -> None:
        """Set a single HSL color attribute of a load.

        Args:
            attribute: The attribute to set the value of.
            value: The value to set the attribute to, 0-360 for hue, 0-100 for
                saturation and lightness.
        """
        # Clamp value to 0-360, 0-100
        if attribute == self.HSLAttribute.Hue:
            value = max(min(value, 360), 0)
        else:
            value = max(min(value, 100), 0)

        # INVOKE <id> RGBLoad.SetHSLAttribute <attribute> <value>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetHSLAttribute <attribute> <value>
        await self.invoke("RGBLoad.SetHSLAttribute", attribute, value)

    async def get_color(self) -> int:
        """Get the RGB/RGBW color of a load from the controller.

        Returns:
            The RGB(W) value of the color as a packed big-endian integer.
        """
        # INVOKE <id> RGBLoad.GetColor
        # -> R:INVOKE <id> <color> RGBLoad.GetColor
        return await self.invoke("RGBLoad.GetColor", as_type=int)

    async def set_rgbw(
        self, red: float, green: float, blue: float, white: float
    ) -> None:
        """Set the color of an RGBW load.

        Args:
            red: The red value of the color, (0-255)
            green: The green value of the color, (0-255)
            blue: The blue value of the color, (0-255)
            white: The white value of the color, (0-255)
        """
        # Clamp levels to 0-255
        red = int(max(min(red, 255), 0))
        green = int(max(min(green, 255), 0))
        blue = int(max(min(blue, 255), 0))
        white = int(max(min(white, 255), 0))

        # INVOKE <id> RGBLoad.SetRGBW <red> <green> <blue> <white>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGBW <red> <green> <blue> <white>
        await self.invoke("RGBLoad.SetRGBW", red, green, blue, white)

    async def get_rgbw(self, channel: int) -> int:
        """Get a single RGBW color channel of a load from the controller.

        Args:
            channel: The channel to get the color of.

        Returns:
            The value of the RGBW channel, 0-255.
        """
        # INVOKE <id> RGBLoad.GetRGBW <channel>
        # -> R:INVOKE <id> <value> RGBLoad.GetRGBW <channel>
        response = await self.invoke(
            "RGBLoad.GetRGBW", channel, as_type=self.ColorChannelResponse
        )
        return response.value

    # Additional convenience methods, not part of the Vantage API
    async def get_rgb_color(self) -> tuple[int, ...]:
        """Get the RGB color of a load from the controller.

        Returns:
            The value of the RGB color as a tuple of (red, green, blue).
        """
        return tuple([await self.get_rgb(attr) for attr in range(3)])

    async def get_rgbw_color(self) -> tuple[int, ...]:
        """Get the RGBW color of a load from the controller.

        Returns:
            The value of the RGBW color as a tuple of (red, green, blue, white).
        """
        return tuple([await self.get_rgbw(chan) for chan in range(4)])

    async def get_hsl_color(self) -> tuple[int, ...]:
        """Get the HSL color of a load from the controller.

        Returns:
            The value of the HSL color as a tuple of (hue, saturation, lightness).
        """
        return tuple([await self.get_hsl(attr) for attr in range(3)])
