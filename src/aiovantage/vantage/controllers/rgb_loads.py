import asyncio
import shlex
import struct
from typing import Sequence

from aiovantage.aci_client.system_objects import DDGColorLoad, DGColorLoad, RGBLoad
from aiovantage.hc_client import StatusType
from aiovantage.vantage.controllers.base import BaseController


# TODO
# - Use ADDSTATUS to get updates for RGBLoad.GetColor and ColorTemperature.Get
# - Update HCClient to support INVOKE command queues

class RGBLoadsController(BaseController[RGBLoad]):
    item_cls = RGBLoad
    vantage_types = (DGColorLoad, DDGColorLoad)
    status_types = (StatusType.LOAD,)

    def _update_object_state(self, vid: int, args: Sequence[str]) -> None:
        if vid not in self:
            return

        print("in _update_object_state", args)
        self[vid].level = float(args[0])

        # RGBLoads only give us the load level in a "STATUS LOAD" status,
        # We could call "ADDSTATUS" for every vid, but ADDSTATUS replies are noisy
        # and have a limit of 64 per connection. Instead, we'll just call
        # RGBLoad.GetColor when an update is available.
        asyncio.create_task(self._fetch_color(vid))

    async def _fetch_color(self, vid: int) -> None:
        if self[vid].color_type == "CCT":
            response = await self._vantage._hc_client.send_command(
                "INVOKE", f"{vid}", "ColorTemperature.Get"
            )
            _, _, temp, _ = shlex.split(response)
            self[vid].color_temp = int(temp)
        else:
            response = await self._vantage._hc_client.send_command(
                "INVOKE", f"{vid}", "RGBLoad.GetColor"
            )
            _, _, color, _ = shlex.split(response)
            r, g, b, w = struct.pack(">i", int(color))
            self[vid].rgb = (r, g, b)

    async def _fetch_object_state(self, vid: int) -> None:
        # Fetch level
        response = await self._vantage._hc_client.send_command("GETLOAD", f"{vid}")
        _, _, level = shlex.split(response)
        self[vid].level = float(level)

        # Fetch color
        # await self._fetch_color(vid)

    async def _fetch_initial_states(self) -> None:
        # Fetch initial state of all Loads.
        await asyncio.gather(*[self._fetch_object_state(load.id) for load in self])

    async def set_level(self, vid: int, level: float) -> None:
        """
        Set the level of a load.

        Args:
            vid: The ID of the load.
            level: The level to set the load to (0-100).
        """

        if vid not in self:
            return

        # Normalize level
        level = max(min(level, 100), 0)

        # Send command to controller
        await self._vantage._hc_client.send_command("LOAD", f"{vid}", f"{level}")

        # Update local level
        self[vid].level = level

    async def set_rgb(
        self, id: int, red: int, green: int, blue: int
    ) -> None:
        """
        Set the color of an RGB load

        Args:
            id: The ID of the load.
            red: The red value (0-255).
            green: The green value (0-255).
            blue: The blue value (0-255).
        """

        await self._vantage._hc_client.send_command(
            "INVOKE",
            f"{id}",
            "RGBLoad.SetRGB",
            f"{red}",
            f"{green}",
            f"{blue}",
        )

    async def set_rgbw(
        self, id: int, red: int, green: int, blue: int, white: int
    ) -> None:
        """
        Set the color of an RGBW load

        Args:
            id: The ID of the load.
            red: The red value (0-255).
            green: The green value (0-255).
            blue: The blue value (0-255).
            white: The white value (0-255).
        """

        await self._vantage._hc_client.send_command(
            "INVOKE",
            f"{id}",
            "RGBLoad.SetRGBW",
            f"{red}",
            f"{green}",
            f"{blue}",
            f"{white}",
        )

    async def set_hsl(self, id: int, hue: int, saturation: int, level: int) -> None:
        """
        Set the color of an HSL load.

        Args:
            id: The ID of the load to set.
            hue: The hue value (0-360).
            saturation: The saturation value (0-100).
            level: The level value (0-100).
        """
        await self._vantage._hc_client.send_command(
            "INVOKE",
            f"{id}",
            "RGBLoad.SetHSL",
            f"{hue}",
            f"{saturation}",
            f"{level}",
        )
