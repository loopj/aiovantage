"""Interface for querying and controlling RGB loads."""

import struct
from typing import Sequence, Tuple

from .base import Interface


class RGBLoadInterface(Interface):
    """Interface for querying and controlling RGB loads."""

    async def get_rgb(self, vid: int) -> Tuple[int, ...]:
        """Get the RGB color of a load from the controller.

        Args:
            vid: The Vantage ID of the RGB load.

        Returns:
            The value of the RGB color as a tuple of (red, green, blue).
        """

        return (await self.get_color(vid))[:3]

    async def get_rgbw(self, vid: int) -> Tuple[int, ...]:
        """Get the RGBW color of a load from the controller.

        Args:
            vid: The Vantage ID of the RGB load.

        Returns:
            The value of the RGBW color as a tuple of (red, green, blue, white).
        """

        return tuple(
            [await self.get_rgbw_channel(vid, channel) for channel in range(4)]
        )

    async def get_hsl(self, vid: int) -> Tuple[int, ...]:
        """Get the HSL color of a load from the controller.

        Args:
            vid: The Vantage ID of the RGB load.

        Returns:
            The value of the HSL color as a tuple of (hue, saturation, lightness).
        """

        return tuple(
            [await self.get_hsl_attribute(vid, attribute) for attribute in range(3)]
        )

    async def get_color(self, vid: int) -> Tuple[int, ...]:
        """Get the RGB/RGBW color of a load from the controller.

        Args:
            vid: The Vantage ID of the RGB load.

        Returns:
            The value of the RGB/RGBW color as a bytearray.
        """

        # INVOKE <id> RGBLoad.GetColor
        # -> R:INVOKE <id> <color> RGBLoad.GetColor
        response = await self.invoke(vid, "RGBLoad.GetColor")
        color = int(response.args[1])

        return tuple(struct.pack(">i", color))

    async def get_rgb_channel(self, vid: int, channel: int) -> int:
        """Get a single RGB color channel of a load from the controller.

        Args:
            vid: The Vantage ID of the RGB load.
            channel: The channel to get the color of.

        Returns:
            The value of the RGB channel, 0-255.
        """

        # INVOKE <id> RGBLoad.GetRGB <channel>
        # -> R:INVOKE <id> <value> RGBLoad.GetRGB <channel>
        response = await self.invoke(vid, "RGBLoad.GetRGB", channel)
        color = int(response.args[1])

        return color

    async def get_rgbw_channel(self, vid: int, channel: int) -> int:
        """Get a single RGBW color channel of a load from the controller.

        Args:
            vid: The Vantage ID of the RGB load.
            channel: The channel to get the color of.

        Returns:
            The value of the RGBW channel, 0-255.
        """

        # INVOKE <id> RGBLoad.GetRGB <channel>
        # -> R:INVOKE <id> <value> RGBLoad.GetRGB <channel>
        response = await self.invoke(vid, "RGBLoad.GetRGBW", channel)
        color = int(response.args[1])

        return color

    async def get_hsl_attribute(self, vid: int, attribute: int) -> int:
        """Get a single HSL color attribute of a load from the controller.

        Args:
            vid: The Vantage ID of the RGB load.
            attribute: The attribute to get the value of.

        Returns:
            The value of the HSL attribute, 0-360 for hue, 0-100 for saturation and
            lightness.
        """

        # INVOKE <id> RGBLoad.GetHSL <channel>
        # -> R:INVOKE <id> <value> RGBLoad.GetHSL <channel>
        response = await self.invoke(vid, "RGBLoad.GetHSL", attribute)
        color = int(response.args[1])

        return color

    async def set_rgb(self, vid: int, red: float, green: float, blue: float) -> None:
        """Set the color of an RGB load.

        Args:
            vid: The Vantage ID of the RGB load.
            red: The red value of the color, (0-255)
            green: The green value of the color, (0-255)
            blue: The blue value of the color, (0-255)
        """

        # Clamp levels to 0-255, ensure they're integers
        red = int(max(min(red, 255), 0))
        green = int(max(min(green, 255), 0))
        blue = int(max(min(blue, 255), 0))

        # INVOKE <id> RGBLoad.SetRGB <red> <green> <blue>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGB <red> <green> <blue>
        await self.invoke(vid, "RGBLoad.SetRGB", red, green, blue)

    async def set_rgbw(
        self, vid: int, red: float, green: float, blue: float, white: float
    ) -> None:
        """Set the color of an RGBW load.

        Args:
            vid: The Vantage ID of the RGB load.
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
        await self.invoke(vid, "RGBLoad.SetRGBW", red, green, blue, white)

    async def set_hsl(
        self, vid: int, hue: float, saturation: float, lightness: float
    ) -> None:
        """Set the color of an HSL load.

        Args:
            vid: The Vantage ID of the RGB load.
            hue: The hue value of the color, in degrees (0-360).
            saturation: The saturation value of the color, in percent (0-100).
            lightness: The lightness value of the color, in percent (0-100).
        """

        # Clamp levels to 0-360, 0-100, ensure they're integers
        hue = int(max(min(hue, 360), 0))
        saturation = int(max(min(saturation, 100), 0))
        lightness = int(max(min(lightness, 100), 0))

        # INVOKE <id> RGBLoad.SetHSL <hue> <saturation> <lightness>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetHSL <hue> <saturation> <lightness>
        await self.invoke(vid, "RGBLoad.SetHSL", hue, saturation, lightness)

    async def dissolve_rgb(
        self, vid: int, red: float, green: float, blue: float, seconds: float
    ) -> None:
        """Transition the color of an RGB load over a number of seconds.

        Args:
            vid: The Vantage ID of the RGB load.
            red: The new red value of the color, (0-255)
            green: The new green value of the color, (0-255)
            blue: The new blue value of the color, (0-255)
            seconds: The number of seconds the transition should take.
        """

        # Clamp levels to 0-255, ensure they're integers
        red = int(max(min(red, 255), 0))
        green = int(max(min(green, 255), 0))
        blue = int(max(min(blue, 255), 0))

        # INVOKE <id> RGBLoad.DissolveRGB <red> <green> <blue>
        # -> R:INVOKE <id> <rcode> RGBLoad.DissolveRGB <red> <green> <blue>
        await self.invoke(vid, "RGBLoad.DissolveRGB", red, green, blue, seconds)

    async def set_rgb_component(self, vid: int, channel: int, value: float) -> None:
        """
        Set a single RGB(W) color channel of a load.

        Args:
            vid: The Vantage ID of the RGB load.
            channel: The channel to set the color of.
            value: The value to set the channel to, 0-255.
        """

        # Clamp levels to 0-255, ensure they're integers
        value = int(max(min(value, 255), 0))

        # INVOKE <id> RGBLoad.SetRGBComponent <channel> <value>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGBComponent <channel> <value>
        await self.invoke(vid, "RGBLoad.SetRGBComponent", channel, value)

    async def dissolve_hsl(
        self, vid: int, hue: float, saturation: float, lightness: float, seconds: float
    ) -> None:
        """Transition the color of an HSL load over a number of seconds.

        Args:
            vid: The Vantage ID of the RGB load.
            hue: The new hue value of the color, in degrees (0-360).
            saturation: The new saturation value of the color, in percent (0-100).
            lightness: The new lightness value of the color, in percent (0-100).
            seconds: The number of seconds the transition should take.
        """

        # Clamp levels to 0-360, 0-100, ensure they're integers
        hue = int(max(min(hue, 360), 0))
        saturation = int(max(min(saturation, 100), 0))
        lightness = int(max(min(lightness, 100), 0))

        # INVOKE <id> RGBLoad.DissolveHSL <hue> <saturation> <lightness>
        # -> R:INVOKE <id> <rcode> RGBLoad.DissolveHSL <hue> <saturation> <lightness>
        await self.invoke(
            vid, "RGBLoad.DissolveHSL", hue, saturation, lightness, seconds
        )

    @classmethod
    def parse_color_channel_status(cls, args: Sequence[str]) -> Tuple[int, int]:
        """Parse an 'RGBLoad.GetRGB' event."""

        # ELLOG STATUSEX ON
        # -> EL: <id> RGBLoad.GetRGB <value> <channel>

        # STATUS ADD <id>
        # -> S:STATUS <id> RGBLoad.GetRGB <value> <channel>
        value = int(args[0])
        channel = int(args[1])

        return channel, value

    @classmethod
    def parse_get_color_status(cls, args: Sequence[str]) -> bytearray:
        """Parse an 'RGBLoad.GetColor' event."""

        # ELLOG STATUS ON
        # -> EL: <id> RGBLoad.GetColor <color>

        # STATUS ADD <id>
        # -> S:STATUS <id> RGBLoad.GetColor <color>
        color = int(args[0])

        return bytearray(struct.pack(">i", color))
