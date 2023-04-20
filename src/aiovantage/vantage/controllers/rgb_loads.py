import struct
from typing import Sequence, Tuple

from aiovantage.aci_client.system_objects import DDGColorLoad, DGColorLoad, RGBLoad
from aiovantage.hc_client import StatusCategory
from aiovantage.vantage.controllers.base import BaseController


def _unpack_color(color: int) -> Tuple[int, int, int, int]:
    bytes = struct.pack(">i", color)
    return struct.unpack("BBBB", bytes)  # type: ignore[return-value]


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
        response = await self._vantage._hc_client.invoke(id, "Load.GetLevel")
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
        response = await self._vantage._hc_client.invoke(id, "RGBLoad.GetColor")
        color = int(response[1])

        return _unpack_color(color)

    async def get_color_temp(self, id: int) -> int:
        """Get the color temperature of a load.

        Args:
            id: The ID of the load.

        Returns:
            The color temperature of the load, in Kelvin.
        """

        # INVOKE <id> ColorTemperature.Get
        # -> R:INVOKE <id> <temp> ColorTemperature.Get
        response = await self._vantage._hc_client.invoke(id, "ColorTemperature.Get")
        color_temp = int(response[1])

        return color_temp

    async def set_level(self, id: int, level: float) -> None:
        """Set the level of a load.

        Args:
            id: The ID of the load.
            level: The level to set the load to, in percent (0-100).
        """

        # INVOKE <id> Load.SetLevel <level>
        # -> R:INVOKE <id> <rcode> Load.SetLevel <level>
        level = max(min(level, 100), 0)
        await self._vantage._hc_client.invoke(id, "Load.SetLevel", level)

        # Update local state
        self[id].level = level

    async def set_rgb(self, id: int, red: int, green: int, blue: int) -> None:
        """Set the color of an RGB load.

        Args:
            id: The ID of the load.
            red: The red value of the color, (0-255)
            green: The green value of the color, (0-255)
            blue: The blue value of the color, (0-255)
        """

        # INVOKE <id> RGBLoad.SetRGB <red> <green> <blue>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGB <red> <green> <blue>
        await self._vantage._hc_client.invoke(id, "RGBLoad.SetRGB", red, green, blue)

        # Update local state
        self[id].color = (red, green, blue, 0)

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

        # INVOKE <id> RGBLoad.SetRGBW <red> <green> <blue> <white>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetRGBW <red> <green> <blue> <white>
        await self._vantage._hc_client.invoke(
            id, "RGBLoad.SetRGBW", red, green, blue, white
        )

        # Update local state
        self[id].color = (red, green, blue, white)

    async def set_hsl(self, id: int, hue: int, saturation: int, level: int) -> None:
        """Set the color of an HSL load.

        Args:
            id: The ID of the load.
            hue: The hue value of the color, in degrees (0-360).
            saturation: The saturation value of the color, in percent (0-100).
            level: The level value of the color, in percent (0-100).
        """

        # INVOKE <id> RGBLoad.SetHSL <hue> <saturation> <level>
        # -> R:INVOKE <id> <rcode> RGBLoad.SetHSL <hue> <saturation> <level>
        await self._vantage._hc_client.invoke(
            id, "RGBLoad.SetHSL", hue, saturation, level
        )

        # Update local state
        # self[id].color = # TODO (use colorsys)

    async def set_color_temp(self, id: int, temp: int) -> None:
        """Set the color temperature of a load.

        Args:
            id: The ID of the load.
            temp: The color temperature to set the load to, in Kelvin.
        """

        # INVOKE <id> ColorTemperature.Set <temp>
        # -> R:INVOKE <id> <rcode> ColorTemperature.Set <temp>
        await self._vantage._hc_client.invoke(id, "ColorTemperature.Set", temp)

        # Update local state
        self[id].color_temp = temp

    async def _fetch_initial_state(self) -> None:
        # Fetch initial state of all RGBLoads.

        for obj in self:
            obj.level = await self.get_level(obj.id)

            if obj.color_type == "CCT":
                obj.color_temp = await self.get_color_temp(obj.id)
            else:
                obj.color = await self.get_color(obj.id)

    def _handle_category_status(
        self, category: StatusCategory, id: int, args: Sequence[str]
    ) -> bool:
        # Update object state based on a "STATUS" events.

        # S:LOAD <id> <level>
        self[id].level = float(args[0])
        return True

    def _handle_object_status(self, id: int, method: str, args: Sequence[str]) -> bool:
        # Update object state based on "ADDSTATUS" events.

        if method == "RGBLoad.GetColor":
            # S:STATUS <id> RGBLoad.GetColor <color>
            self[id].color = _unpack_color(int(args[0]))
            return True
        elif method == "ColorTemperature.Get":
            # S:STATUS <id> ColorTemperature.Get <temp>
            self[id].color_temp = int(args[0])
            return True

        return False
