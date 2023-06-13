import struct
from typing import Sequence, Tuple

from .base import Interface


class RGBLoadInterface(Interface):
    async def get_rgb(self, id: int) -> Tuple[int, ...]:
        """
        Get the RGB color of a load from the controller.

        Args:
            id: The ID of the load.

        Returns:
            The value of the RGB color as a tuple of (red, green, blue).
        """

        return (await self.get_color(id))[:3]

    async def get_rgbw(self, id: int) -> Tuple[int, ...]:
        """
        Get the RGBW color of a load from the controller.

        Args:
            id: The ID of the load.

        Returns:
            The value of the RGBW color as a tuple of (red, green, blue, white).
        """

        return tuple([await self.get_rgb_channel(id, channel) for channel in range(4)])

    async def get_hsl(self, id: int) -> Tuple[int, ...]:
        """
        Get the HSL color of a load from the controller.

        Args:
            id: The ID of the load.

        Returns:
            The value of the HSL color as a tuple of (hue, saturation, lightness).
        """

        return tuple(
            [await self.get_hsl_attribute(id, attribute) for attribute in range(3)]
        )

    async def get_color(self, id: int) -> Tuple[int, ...]:
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

        return tuple(struct.pack(">i", color))

    async def get_rgb_channel(self, id: int, channel: int) -> int:
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
        response = await self.invoke(id, "RGBLoad.GetRGB", channel)
        color = int(response.args[1])

        return color

    async def get_rgbw_channel(self, id: int, channel: int) -> int:
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
        response = await self.invoke(id, "RGBLoad.GetRGBW", channel)
        color = int(response.args[1])

        return color

    async def get_hsl_attribute(self, id: int, attribute: int) -> int:
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
        response = await self.invoke(id, "RGBLoad.GetHSL", attribute)
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

    @classmethod
    def parse_color_channel_status(cls, args: Sequence[str]) -> Tuple[int, int]:
        # ELLOG STATUSEX ON
        # -> EL: <id> RGBLoad.GetRGB <value> <channel>

        # STATUS ADD <id>
        # -> S:STATUS <id> RGBLoad.GetRGB <value> <channel>
        value = int(args[0])
        channel = int(args[1])

        return (channel, value)

    @classmethod
    def parse_get_color_status(cls, args: Sequence[str]) -> bytearray:
        # ELLOG STATUS ON
        # -> EL: <id> RGBLoad.GetColor <color>

        # STATUS ADD <id>
        # -> S:STATUS <id> RGBLoad.GetColor <color>
        color = int(args[0])

        return bytearray(struct.pack(">i", color))
