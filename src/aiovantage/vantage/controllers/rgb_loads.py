import colorsys
import struct
from typing import TYPE_CHECKING, Any, Dict, List, Sequence, Tuple

from aiovantage.aci_client.system_objects import DDGColorLoad, DGColorLoad, RGBLoad
from aiovantage.hc_client import StatusCategory
from aiovantage.vantage.controllers.base import BaseController

if TYPE_CHECKING:
    from aiovantage import Vantage


def _unpack_color(color: int) -> Tuple[int, int, int, int]:
    bytes = struct.pack(">i", color)
    return struct.unpack("BBBB", bytes)  # type: ignore[return-value]


def _hs_to_rgb(hue: int, saturation: int) -> Tuple[int, int, int]:
    rgb = colorsys.hsv_to_rgb(hue / 360, saturation / 100, 1)
    return tuple(int(x * 255) for x in rgb)  # type: ignore[return-value]


class RGBLoadsController(BaseController[RGBLoad]):
    item_cls = RGBLoad
    vantage_types = (DGColorLoad, DDGColorLoad)
    status_categories = (StatusCategory.LOAD,)
    object_status = True

    def __init__(self, vantage: "Vantage") -> None:
        super().__init__(vantage)

        self._temp_color_map: Dict[int, List[int]] = {}

    async def get_level(self, id: int) -> float:
        """Get the level of a load.

        Args:
            id: The ID of the load.

        Returns:
            The level of the load, in percent (0-100).
        """

        # INVOKE <id> Load.GetLevel
        # -> R:INVOKE <id> <level> Load.GetLevel
        response = await self.command_client.invoke(id, "Load.GetLevel")
        level = float(response[1])

        return level

    async def get_color(self, id: int) -> Tuple[int, int, int, int]:
        """Get the color of a load.

        Args:
            id: The ID of the load.

        Returns:
            The color of the load, as a tuple of values between 0-255.
        """

        # INVOKE <id> RGBLoad.GetColor
        # -> R:INVOKE <id> <color> RGBLoad.GetColor
        response = await self.command_client.invoke(id, "RGBLoad.GetColor")
        color = int(response[1])

        return _unpack_color(color)

    async def get_color_rgbw(self, id: int) -> Tuple[int, int, int, int]:
        tmp_color = []
        for i in range(4):
            response = await self.command_client.invoke(id, "RGBLoad.GetRGBW", i)
            tmp_color.append(int(response[1]))

        return tuple(tmp_color)  # type: ignore[return-value]

    async def get_color_temp(self, id: int) -> int:
        """Get the color temperature of a load.

        Args:
            id: The ID of the load.

        Returns:
            The color temperature of the load, in Kelvin.
        """

        # INVOKE <id> ColorTemperature.Get
        # -> R:INVOKE <id> <temp> ColorTemperature.Get
        response = await self.command_client.invoke(id, "ColorTemperature.Get")
        color_temp = int(response[1])

        return color_temp

    async def set_level(self, id: int, level: float) -> None:
        """Set the level of a load.

        Args:
            id: The ID of the load.
            level: The level to set the load to, in percent (0-100).
        """

        # Clamp level to 0-100
        level = round(max(min(level, 100), 0))

        # Don't send a command if the level isn't changing
        if self[id].level == level:
            return

        # INVOKE <id> Load.SetLevel <level>
        # -> R:INVOKE <id> <rcode> Load.SetLevel <level>
        await self.command_client.invoke(id, "Load.SetLevel", level)

        # Update local state
        self._update_and_notify(id, level=level)

    async def set_rgb(self, id: int, red: int, green: int, blue: int) -> None:
        """Set the color of an RGB load.

        Args:
            id: The ID of the load.
            red: The red value of the color, (0-255)
            green: The green value of the color, (0-255)
            blue: The blue value of the color, (0-255)
        """

        # Clamp levels to 0-255
        red = max(min(red, 255), 0)
        green = max(min(green, 255), 0)
        blue = max(min(blue, 255), 0)

        # Don't send a command if the color isn't changing
        if self[id].color == (red, green, blue, 0):
            return

        # INVOKE <id> RGBLoad.SetRGB <red> <green> <blue>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGB <red> <green> <blue>
        await self.command_client.invoke(id, "RGBLoad.SetRGB", red, green, blue)

        # Update local state
        self._update_and_notify(id, color=(red, green, blue, 0))

    async def set_rgbw(
        self, id: int, red: int, green: int, blue: int, white: int
    ) -> None:
        """Set the color of an RGBW load.

        Args:
            id: The ID of the load.
            red: The red value of the color, (0-255)
            green: The green value of the color, (0-255)
            blue: The blue value of the color, (0-255)
            white: The white value of the color, (0-255)
        """

        # Clamp levels to 0-255
        red = max(min(red, 255), 0)
        green = max(min(green, 255), 0)
        blue = max(min(blue, 255), 0)
        white = max(min(white, 255), 0)

        # Don't send a command if the color isn't changing
        if self[id].color == (red, green, blue, white):
            return

        # INVOKE <id> RGBLoad.SetRGBW <red> <green> <blue> <white>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGBW <red> <green> <blue> <white>
        await self.command_client.invoke(id, "RGBLoad.SetRGBW", red, green, blue, white)

        # Update local state
        self._update_and_notify(id, color=(red, green, blue, white))

    async def set_hsl(self, id: int, hue: int, saturation: int, level: int) -> None:
        """Set the color of an HSL load.

        Args:
            id: The ID of the load.
            hue: The hue value of the color, in degrees (0-360).
            saturation: The saturation value of the color, in percent (0-100).
            level: The level value of the color, in percent (0-100).
        """

        # Clamp levels to 0-360, 0-100
        hue = max(min(hue, 360), 0)
        saturation = max(min(saturation, 100), 0)
        level = max(min(level, 100), 0)

        # Get the rgb equivalent of the hsl values
        rgb = _hs_to_rgb(hue, saturation) + (0,)

        # Don't send a command if the color isn't changing
        if self[id].color == rgb:
            return

        # INVOKE <id> RGBLoad.SetHSL <hue> <saturation> <level>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetHSL <hue> <saturation> <level>
        await self.command_client.invoke(id, "RGBLoad.SetHSL", hue, saturation, level)

        # Update local state
        self._update_and_notify(id, color=rgb)

    async def set_color_temp(self, id: int, temp: int) -> None:
        """Set the color temperature of a load.

        Args:
            id: The ID of the load.
            temp: The color temperature to set the load to, in Kelvin.
        """

        # Don't send a command if the color temperature isn't changing
        if self[id].color_temp == temp:
            return

        # INVOKE <id> ColorTemperature.Set <temp>
        # -> R:INVOKE <id> <rcode> ColorTemperature.Set <temp>
        await self.command_client.invoke(id, "ColorTemperature.Set", temp)

        # Update local state
        self._update_and_notify(id, color_temp=temp)

    async def _fetch_initial_state(self, id: int) -> None:
        # Populate the initial state of an RGBLoad.

        # Get initial level
        state: Dict[str, Any] = {}
        state["level"] = await self.get_level(id)

        # Get initial color
        color_type = self[id].color_type
        if color_type == "RGB" or color_type == "HSL":
            state["color"] = await self.get_color(id)
        elif color_type == "CCT":
            state["color_temp"] = await self.get_color_temp(id)
        elif color_type == "RGBW":
            state["color"] = await self.get_color_rgbw(id)
        else:
            self._logger.warning(f"Unsupported color type: {color_type}")

        self._update_and_notify(id, **state)

    def _handle_category_status(
        self, id: int, category: StatusCategory, args: Sequence[str]
    ) -> None:
        # Update object state based on a "STATUS" events.

        # S:LOAD <id> <level>
        self._update_and_notify(id, level=float(args[0]))

    def _handle_object_status(self, id: int, method: str, args: Sequence[str]) -> None:
        # Update object state based on "ADDSTATUS" events.

        color_type = self[id].color_type
        if method == "RGBLoad.GetColor":
            # S:STATUS <id> RGBLoad.GetColor <color>

            # RGBLoad.GetColor works great for both RGB and HSL loads.
            if color_type != "RGB" and color_type != "HSL":
                return

            self._update_and_notify(id, color=_unpack_color(int(args[0])))

        elif method == "RGBLoad.GetRGBW":
            # S:STATUS <id> RGBLoad.GetRBGW <value> <channel>

            # For some annoying reason RGBLoad.GetColor doesn't contain the white
            # value, so we have to grab each channel individually from RGBLoad.GetRGBW.

            # Apply only to RGBW loads
            if color_type != "RGBW":
                return

            if id not in self._temp_color_map:
                self._temp_color_map[id] = [0, 0, 0, 0]

            channel = int(args[1])
            self._temp_color_map[id][channel] = int(args[0])

            if channel == 3:
                self._update_and_notify(id, color=tuple(self._temp_color_map[id]))
                del self._temp_color_map[id]

        elif method == "ColorTemperature.Get":
            # S:STATUS <id> ColorTemperature.Get <temp>

            # Apply only to CCT loads
            if color_type != "CCT":
                return

            self._update_and_notify(id, color_temp=int(args[0]))
