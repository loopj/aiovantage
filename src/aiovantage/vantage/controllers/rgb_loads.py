import struct
from typing import Any, Dict, List, Sequence, Tuple

from typing_extensions import override

from aiovantage.aci_client import ACIClient
from aiovantage.aci_client.system_objects import DDGColorLoad, DGColorLoad, RGBLoad
from aiovantage.hc_client import HCClient
from aiovantage.vantage.controllers.base import StatefulController


def _unpack_color(color: int) -> Tuple[int, int, int, int]:
    bytes = struct.pack(">i", color)
    return struct.unpack("BBBB", bytes)  # type: ignore[return-value]


class RGBLoadsController(StatefulController[RGBLoad]):
    item_cls = RGBLoad
    vantage_types = (DGColorLoad, DDGColorLoad)
    event_log_status = True

    def __init__(self, aci_client: ACIClient, hc_client: HCClient) -> None:
        super().__init__(aci_client, hc_client)

        self._temp_color_map: Dict[int, List[int]] = {}

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
        response = await self._hc_client.invoke(id, "Load.GetLevel")
        level = float(response[1])

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
        response = await self._hc_client.invoke(id, "RGBLoad.GetColor")
        color = int(response[1])

        return _unpack_color(color)[:3]

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
            response = await self._hc_client.invoke(id, "RGBLoad.GetRGBW", i)
            rgbw_values.append(int(response[1]))

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
            response = await self._hc_client.invoke(id, "RGBLoad.GetHSL", i)
            hsl_values.append(int(response[1]))

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
        response = await self._hc_client.invoke(id, "ColorTemperature.Get")
        color_temp = int(response[1])

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
        await self._hc_client.invoke(id, "Load.SetLevel", level)

        # Update local state
        self.update_state(id, {"level": level})

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

        # Don't send a command if the color isn't changing
        if id in self and self[id].rgb == (red, green, blue):
            return

        # TODO: Use DissolveRGB for transitions

        # INVOKE <id> RGBLoad.SetRGB <red> <green> <blue>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGB <red> <green> <blue>
        await self._hc_client.invoke(id, "RGBLoad.SetRGB", red, green, blue)

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
        await self._hc_client.invoke(id, "RGBLoad.SetRGBW", red, green, blue, white)

        # Update local state
        self.update_state(id, {"rgbw": (red, green, blue, white)})

    async def set_hsl(self, id: int, hue: int, saturation: int, level: int) -> None:
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

        # TODO: Use DissolveHSL for transitions

        # INVOKE <id> RGBLoad.SetHSL <hue> <saturation> <level>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetHSL <hue> <saturation> <level>
        await self._hc_client.invoke(id, "RGBLoad.SetHSL", hue, saturation, level)

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

        # INVOKE <id> ColorTemperature.Set <temp>
        # -> R:INVOKE <id> <rcode> ColorTemperature.Set <temp>
        await self._hc_client.invoke(id, "ColorTemperature.Set", temp, transition)

        # Update local state
        self.update_state(id, {"color_temp": temp})

    @override
    async def fetch_initial_state(self, id: int) -> None:
        # Populate the initial state of an RGBLoad.

        state: Dict[str, Any] = {}

        # Get initial color
        color_type = self[id].color_type
        if color_type == "HSL":
            hsl = await self.get_hsl(id)
            state["hs"] = hsl[:2]
            state["level"] = hsl[2]
        elif color_type == "CCT":
            state["color_temp"] = await self.get_color_temp(id)
            state["level"] = await self.get_level(id)
        elif color_type == "RGB":
            state["rgb"] = await self.get_rgb(id)
        elif color_type == "RGBW":
            state["rgbw"] = await self.get_rgbw(id)
        else:
            self._logger.warning(f"Unsupported color type: {color_type}")

        self.update_state(id, state)

    @override
    def handle_state_change(self, id: int, status: str, args: Sequence[str]) -> None:
        # Handle state changes for an RGBLoad.

        state: Dict[str, Any] = {}
        color_type = self[id].color_type

        if status == "Load.GetLevel":
            # <id> Load.GetLevel <level (0-100000)>

            if color_type != "CCT":
                return

            state["level"] = int(args[0]) / 1000

        elif status == "RGBLoad.GetColor":
            # <id> RGBLoad.GetColor <color)>

            if color_type != "RGB":
                return

            state["rgb"] = _unpack_color(int(args[0]))[:3]

        elif status == "RGBLoad.GetHSL":
            # <id> RGBLoad.GetHSL <value> <channel>

            if color_type != "HSL":
                return

            if id not in self._temp_color_map:
                self._temp_color_map[id] = [0, 0, 0]

            channel = int(args[1])
            self._temp_color_map[id][channel] = int(args[0])

            if channel == 2:
                state["hs"] = tuple(self._temp_color_map[id][:2])
                state["level"] = self._temp_color_map[id][2]

                del self._temp_color_map[id]

        elif status == "RGBLoad.GetRGBW":
            # <id> RGBLoad.GetRGBW <value> <channel>

            if color_type != "RGBW":
                return

            if id not in self._temp_color_map:
                self._temp_color_map[id] = [0, 0, 0, 0]

            channel = int(args[1])
            self._temp_color_map[id][channel] = int(args[0])

            if channel == 3:
                state["rgbw"] = tuple(self._temp_color_map[id])

                del self._temp_color_map[id]

        elif status == "ColorTemperature.Get":
            # <id> ColorTemperature.Get <temp>

            if color_type != "CCT":
                return

            state["color_temp"] = int(args[0])

        self.update_state(id, state)
