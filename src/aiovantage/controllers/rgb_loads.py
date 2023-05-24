import struct
from typing import Any, Dict, List, Optional, Sequence, Tuple

from typing_extensions import override

from aiovantage.config_client.objects import DDGColorLoad, DGColorLoad, RGBLoad
from aiovantage.controllers.base import StatefulController


class RGBLoadsController(StatefulController[RGBLoad]):
    # Store objects managed by this controller as RGBLoad instances
    item_cls = RGBLoad

    # Fetch Vantage.DGColorLoad and Vantage.DDGColorLoad objects from Vantage
    vantage_types = (DGColorLoad, DDGColorLoad)

    # Get status updates from the event log
    event_log_status = True

    async def initialize(self) -> None:
        self._temp_color_map: Dict[int, List[int]] = {}
        return await super().initialize()

    async def get_level(self, id: int) -> float:
        """
        Get the level of a load from the controller.

        Args:
            id: The ID of the load.

        Returns:
            The level of the load, between 0-100.
        """

        # INVOKE <id> Load.GetLevel
        # -> R:INVOKE <id> <level> Load.GetLevel
        response = await self.command_client.command("INVOKE", id, "Load.GetLevel")
        level = float(response.args[1])

        return level

    async def get_rgb(self, id: int) -> Tuple[int, int, int]:
        """
        Get the RGB color of a load from the controller.

        Args:
            id: The ID of the load.

        Returns:
            The color of the load, as a tuple of values between 0-255.
        """

        # INVOKE <id> RGBLoad.GetColor
        # -> R:INVOKE <id> <color> RGBLoad.GetColor
        response = await self.command_client.command("INVOKE", id, "RGBLoad.GetColor")
        color = int(response.args[1])

        return self._unpack_color_int(color)[:3]

    async def get_rgbw(self, id: int) -> Tuple[int, int, int, int]:
        """
        Get the RGBW color of a load from the controller.

        Args:
            id: The ID of the load.

        Returns:
            The color of the load, as a tuple of values between 0-255.
        """

        # INVOKE <id> RGBLoad.GetRGBW <index>
        # -> R:INVOKE <id> <value> RGBLoad.GetRGBW <index>
        rgbw_values = []
        for i in range(4):
            response = await self.command_client.command(
                "INVOKE", id, "RGBLoad.GetRGBW", i
            )
            rgbw_values.append(int(response.args[1]))

        return tuple(rgbw_values)  # type: ignore[return-value]

    async def get_hsl(self, id: int) -> Tuple[int, int, int]:
        """
        Get the HSL color of a load from the controller.

        Args:
            id: The ID of the load.

        Returns:
            The color of the load, as a tuple of values 0-360, 0-100, 0-100.
        """

        # INVOKE <id> RGBLoad.GetHSL <index>
        # -> R:INVOKE <id> <value> RGBLoad.GetHSL <index>
        hsl_values = []
        for i in range(3):
            response = await self.command_client.command(
                "INVOKE", id, "RGBLoad.GetHSL", i
            )
            hsl_values.append(int(response.args[1]))

        return tuple(hsl_values)  # type: ignore[return-value]

    async def get_color_temp(self, id: int) -> int:
        """
        Get the color temperature of a load.

        Args:
            id: The ID of the load.

        Returns:
            The color temperature of the load, in Kelvin.
        """

        # INVOKE <id> ColorTemperature.Get
        # -> R:INVOKE <id> <temp> ColorTemperature.Get
        response = await self.command_client.command(
            "INVOKE", id, "ColorTemperature.Get"
        )
        color_temp = int(response.args[1])

        return color_temp

    async def set_level(self, id: int, level: float) -> None:
        """
        Set the level of a load.

        Args:
            id: The ID of the load.
            level: The level of the load, between 0-100.
        """

        # Clamp level to 0-100, match the precision of the controller
        level = round(max(min(level, 100), 0), 3)

        # Don't send a command if the level isn't changing
        if id in self and self[id].level == level:
            return

        # INVOKE <id> Load.SetLevel <level>
        # -> R:INVOKE <id> <rcode> Load.SetLevel <level>
        await self.command_client.command("INVOKE", id, "Load.SetLevel", level)

        # Update local state
        self.update_state(id, {"level": level})

    async def set_rgb(
        self, id: int, red: int, green: int, blue: int, transition: float = 0
    ) -> None:
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

        # Don't send a command if the color isn't changing
        if id in self and self[id].rgb == (red, green, blue):
            return

        if transition:
            # INVOKE <id> RGBLoad.DissolveRGB <red> <green> <blue> <seconds>
            # -> R:INVOKE <id> <rcode> RGBLoad.DissolveRGB <red> <green> <blue> <seconds
            await self.command_client.command(
                "INVOKE", id, "RGBLoad.DissolveRGB", red, green, blue, transition
            )
        else:
            # INVOKE <id> RGBLoad.SetRGB <red> <green> <blue>
            # -> R:INVOKE <id> <rcode> RGBLoad.SetRGB <red> <green> <blue>
            await self.command_client.command(
                "INVOKE", id, "RGBLoad.SetRGB", red, green, blue
            )

        # Update local state
        self.update_state(id, {"rgb": (red, green, blue)})

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

        # Don't send a command if the color isn't changing
        if id in self and self[id].rgbw == (red, green, blue, white):
            return

        # INVOKE <id> RGBLoad.SetRGBW <red> <green> <blue> <white>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGBW <red> <green> <blue> <white>
        await self.command_client.command(
            "INVOKE", id, "RGBLoad.SetRGBW", red, green, blue, white
        )

        # Update local state
        self.update_state(id, {"rgbw": (red, green, blue, white)})

    async def set_hsl(
        self, id: int, hue: int, saturation: int, level: int, transition: float = 0
    ) -> None:
        """
        Set the color of an HSL load.

        Args:
            id: The ID of the load.
            hue: The hue value of the color, in degrees (0-360).
            saturation: The saturation value of the color, in percent (0-100).
            level: The level value of the color, in percent (0-100).
        """

        # Clamp levels to 0-360, 0-100, ensure they're integers
        hue = int(max(min(hue, 360), 0))
        saturation = int(max(min(saturation, 100), 0))
        level = int(max(min(level, 100), 0))

        # Don't send a command if the color isn't changing
        if id in self and self[id].hs == (hue, saturation) and self[id].level == level:
            return

        if transition:
            # INVOKE <id> RGBLoad.DissolveHSL <hue> <saturation> <level> <seconds>
            # -> R:INVOKE <id> <rcode> RGBLoad.DissolveHSL <hue> <sat> <level> <seconds>
            await self.command_client.command(
                "INVOKE", id, "RGBLoad.DissolveHSL", hue, saturation, level, transition
            )
        else:
            # INVOKE <id> RGBLoad.SetHSL <hue> <saturation> <level>
            # -> R:INVOKE <id> <rcode> RGBLoad.SetHSL <hue> <saturation> <level>
            await self.command_client.command(
                "INVOKE", id, "RGBLoad.SetHSL", hue, saturation, level
            )

        # Update local state
        self.update_state(id, {"hs": (hue, saturation), "level": level})

    async def set_color_temp(self, id: int, temp: int, transition: int = 0) -> None:
        """
        Set the color temperature of a load.

        Args:
            id: The ID of the load.
            temp: The color temperature to set the load to, in Kelvin.
            transition: The time in seconds to transition to the new color
        """

        # Ensure the temperature is an integer
        temp = int(temp)

        # Don't send a command if the color temperature isn't changing
        if id in self and self[id].color_temp == temp:
            return

        # INVOKE <id> ColorTemperature.Set <temp> <seconds>
        # -> R:INVOKE <id> <rcode> ColorTemperature.Set <temp>
        await self.command_client.command(
            "INVOKE", id, "ColorTemperature.Set", temp, transition
        )

        # Update local state
        self.update_state(id, {"color_temp": temp})

    @override
    async def fetch_object_state(self, id: int) -> None:
        # Fetch initial state of an RGBLoad.

        state: Dict[str, Any] = {}
        color_type = self[id].color_type

        # We care about HSL values for HSL, RGB, and RGBW loads, since color
        # information is lost in the rgb values when adjusting brightness/level.
        if color_type == "HSL" or color_type == "RGB" or color_type == "RGBW":
            hsl = await self.get_hsl(id)
            state["hs"] = hsl[:2]
            state["level"] = hsl[2]

        if color_type == "RGB":
            state["rgb"] = await self.get_rgb(id)

        if color_type == "RGBW":
            state["rgbw"] = await self.get_rgbw(id)

        if color_type == "CCT":
            state["color_temp"] = await self.get_color_temp(id)
            state["level"] = await self.get_level(id)

        self.update_state(id, state)

    @override
    def handle_object_update(self, id: int, status: str, args: Sequence[str]) -> None:
        # Handle state changes for an RGBLoad.

        state: Dict[str, Any] = {}
        color_type = self[id].color_type

        if status == "RGBLoad.GetHSL":
            # <id> RGBLoad.GetHSL <value> <channel>

            # We care about HS values for RGB, and RGBW loads, since color information
            # is lost in the rgb values when adjusting brightness/level.
            if not (color_type == "HSL" or color_type == "RGB" or color_type == "RGBW"):
                return

            # Build a color from each HSL channel
            hsl = self._build_color_from_channels(id, args, num_channels=3)
            if hsl is not None:
                state["hs"] = hsl[:2]
                state["level"] = hsl[2]

        elif status == "RGBLoad.GetColor":
            # <id> RGBLoad.GetColor <color)>

            if color_type != "RGB":
                return

            state["rgb"] = self._unpack_color_int(int(args[0]))[:3]

        elif status == "RGBLoad.GetRGBW":
            # <id> RGBLoad.GetRGBW <value> <channel>

            # We only care about RGBW values for RGBW loads
            if color_type != "RGBW":
                return

            # Build a color from each RGBW channel
            color = self._build_color_from_channels(id, args, num_channels=4)
            if color is not None:
                state["rgbw"] = color

        elif status == "ColorTemperature.Get":
            # <id> ColorTemperature.Get <temp>

            # We only care about color temperature for CCT loads
            if color_type != "CCT":
                return

            state["color_temp"] = int(args[0])

        elif status == "Load.GetLevel":
            # <id> Load.GetLevel <level (0-100000)>

            # We only care about level changes for CCT loads
            if color_type != "CCT":
                return

            state["level"] = int(args[0]) / 1000

        self.update_state(id, state)

    def _build_color_from_channels(
        self, id: int, args: Sequence[str], num_channels: int
    ) -> Optional[Tuple[int, ...]]:
        # Build a color from a series of channel values. We need to store partially
        # constructed colors in memory, since updates come separately for each channel.

        if id not in self._temp_color_map:
            self._temp_color_map[id] = num_channels * [0]

        # Extract the color and channel from the args
        channel = int(args[1])
        self._temp_color_map[id][channel] = int(args[0])

        # If we have all the channels, build and return the color
        if channel == num_channels - 1:
            color = tuple(self._temp_color_map[id])
            del self._temp_color_map[id]
            return color

        return None

    def _unpack_color_int(self, color: int) -> Tuple[int, int, int, int]:
        # Unpack a signed 32-bit integer from RGBLoad.GetColor into a color tuple

        bytes = struct.pack(">i", color)
        return struct.unpack("BBBB", bytes)  # type: ignore[return-value]
