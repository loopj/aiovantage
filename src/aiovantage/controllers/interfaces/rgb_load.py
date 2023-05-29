import struct
from enum import Enum
from typing import Tuple

from . import Interface


class RGBLoadInterface(Interface):
    class RGBChannel(Enum):
        RED = 0
        GREEN = 1
        BLUE = 2
        WHITE = 3

    class HSLAttribute(Enum):
        HUE = 0
        SATURATION = 1
        LIGHTNESS = 2

    async def get_rgb(self, id: int) -> bytearray:
        """
        Get the RGB color of a load from the controller.

        Args:
            id: The ID of the load.

        Returns:
            The value of the RGB color as a bytearray.
        """

        return bytearray(
            [
                await self.get_rgb_channel(id, channel)
                for channel in list(self.RGBChannel)[:3]
            ]
        )

    async def get_rgbw(self, id: int) -> bytearray:
        """
        Get the RGBW color of a load from the controller.

        Args:
            id: The ID of the load.

        Returns:
            The value of the RGBW color as a bytearray.
        """

        return bytearray(
            [await self.get_rgb_channel(id, channel) for channel in self.RGBChannel]
        )

    async def get_hsl(self, id: int) -> Tuple[int, ...]:
        """
        Get the HSL color of a load from the controller.

        Args:
            id: The ID of the load.

        Returns:
            The value of the HSL color as a tuple of (hue, saturation, lightness).
        """

        return tuple(
            [
                await self.get_hsl_attribute(id, attribute)
                for attribute in self.HSLAttribute
            ]
        )

    async def get_color(self, id: int) -> bytearray:
        """
        Get the RGB/RGBW color of a load from the controller.

        Args:
            id: The ID of the load.

        Returns:
            The value of the RGB/RGBW color as a bytearray.
        """

        # INVOKE <id> RGBLoad.GetColor
        # -> R:INVOKE <id> <color> RGBLoad.GetColor
        response = await self.invoke(id, "RGBLoad.GetColor")
        color = int(response.args[1])

        return bytearray(struct.pack(">i", color))

    async def get_rgb_channel(self, id: int, channel: RGBChannel) -> int:
        """
        Get a single RGB color channel of a load from the controller.

        Args:
            id: The ID of the load.
            channel: The channel to get the color of.

        Returns:
            The value of the RGB channel, 0-255.
        """

        # INVOKE <id> RGBLoad.GetRGB <channel>
        # -> R:INVOKE <id> <value> RGBLoad.GetRGB <channel>
        response = await self.invoke(id, "RGBLoad.GetRGB", channel.value)
        color = int(response.args[1])

        return color

    async def get_rgbw_channel(self, id: int, channel: RGBChannel) -> int:
        """
        Get a single RGBW color channel of a load from the controller.

        Args:
            id: The ID of the load.
            channel: The channel to get the color of.

        Returns:
            The value of the RGBW channel, 0-255.
        """

        # INVOKE <id> RGBLoad.GetRGB <channel>
        # -> R:INVOKE <id> <value> RGBLoad.GetRGB <channel>
        response = await self.invoke(id, "RGBLoad.GetRGBW", channel.value)
        color = int(response.args[1])

        return color

    async def get_hsl_attribute(self, id: int, attribute: HSLAttribute) -> int:
        """
        Get a single HSL color attribute of a load from the controller.

        Args:
            id: The ID of the load.
            attribute: The attribute to get the value of.

        Returns:
            The value of the HSL attribute, 0-360 for hue, 0-100 for saturation and
            lightness.
        """

        # INVOKE <id> RGBLoad.GetHSL <channel>
        # -> R:INVOKE <id> <value> RGBLoad.GetHSL <channel>
        response = await self.invoke(id, "RGBLoad.GetHSL", attribute.value)
        color = int(response.args[1])

        return color

    async def set_rgb(self, id: int, red: int, green: int, blue: int) -> None:
        """
        Set the color of an RGB load.

        Args:
            id: The ID of the load.
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
        await self.invoke(id, "RGBLoad.SetRGB", red, green, blue)

    async def set_rgbw(
        self, id: int, red: int, green: int, blue: int, white: int
    ) -> None:
        """
        Set the color of an RGBW load.

        Args:
            id: The ID of the load.
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
        await self.invoke(id, "RGBLoad.SetRGBW", red, green, blue, white)

    async def set_hsl(self, id: int, hue: int, saturation: int, lightness: int) -> None:
        """
        Set the color of an HSL load.

        Args:
            id: The ID of the load.
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
        await self.invoke(id, "RGBLoad.SetHSL", hue, saturation, lightness)

    async def dissolve_rgb(
        self, id: int, red: int, green: int, blue: int, seconds: int
    ) -> None:
        """
        Transition the color of an RGB load over a number of seconds.

        Args:
            id: The ID of the load.
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
        await self.invoke(id, "RGBLoad.DissolveRGB", red, green, blue, seconds)

    async def dissolve_hsl(
        self, id: int, hue: int, saturation: int, lightness: int, seconds: int
    ) -> None:
        """
        Transition the color of an HSL load over a number of seconds.

        Args:
            id: The ID of the load.
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
            id, "RGBLoad.DissolveHSL", hue, saturation, lightness, seconds
        )
