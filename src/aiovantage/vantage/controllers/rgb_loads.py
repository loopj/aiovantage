import colorsys
import struct
from typing import Sequence, Tuple

from aiovantage.aci_client.system_objects import DDGColorLoad, DGColorLoad, RGBLoad
from aiovantage.hc_client import StatusCategory
from aiovantage.vantage.controllers.base import BaseController


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

        return tuple(tmp_color) # type: ignore[return-value]

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
        self._update_state(id, level=level)

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
        self._update_state(id, color=(red, green, blue, 0))

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
        print("in set_rgbw")
        self._update_state(id, color=(red, green, blue, white))

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
        rgb = _hs_to_rgb(hue, saturation)

        # Don't send a command if the color isn't changing
        if self[id].color == rgb + (0,):
            return

        # INVOKE <id> RGBLoad.SetHSL <hue> <saturation> <level>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetHSL <hue> <saturation> <level>
        await self.command_client.invoke(id, "RGBLoad.SetHSL", hue, saturation, level)

        # Update local state
        self._update_state(id, color=rgb)

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
        self._update_state(id, color_temp=temp)

    async def _fetch_initial_state(self) -> None:
        # Fetch initial state of all RGBLoads.

        for obj in self:
            obj.level = await self.get_level(obj.id)
            if obj.color_type == "CCT":
                obj.color_temp = await self.get_color_temp(obj.id)
            elif obj.color_type == "RGBW":
                obj.color = await self.get_color_rgbw(obj.id)
            else:
                obj.color = await self.get_color(obj.id)

    def _handle_category_status(
        self, category: StatusCategory, id: int, args: Sequence[str]
    ) -> None:
        # Update object state based on a "STATUS" events.

        # S:LOAD <id> <level>
        self._update_state(id, level=float(args[0]))

    def _handle_object_status(self, id: int, method: str, args: Sequence[str]) -> None:
        # Update object state based on "ADDSTATUS" events.

        if method == "RGBLoad.GetColor" and self[id].color_type == "RGB" or self[id].color_type == "HSL":
            # S:STATUS <id> RGBLoad.GetColor <color>
            self._update_state(id, color=_unpack_color(int(args[0])))
        elif method == "RGBLoad.GetRGBW" and self[id].color_type == "RGBW":
            # S:STATUS <id> RGBLoad.GetRBGW <value> <channel>
            if self[id]._temp_color is None:
                self[id]._temp_color = [0,0,0,0]

            val = int(args[0])
            channel = int(args[1])

            self[id]._temp_color[channel] = val

            if channel == 3:
                self._update_state(id, color=tuple(self[id]._temp_color))
                self[id]._temp_color = None

        elif method == "ColorTemperature.Get" and self[id].color_type == "CCT":
            # S:STATUS <id> ColorTemperature.Get <temp>
            self._update_state(id, color_temp=int(args[0]))
