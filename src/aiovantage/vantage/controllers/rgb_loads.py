import asyncio
import shlex
import struct
from typing import Sequence

from aiovantage.aci_client.system_objects import DDGColorLoad, DGColorLoad, RGBLoad
from aiovantage.hc_client import StatusType
from aiovantage.vantage.controllers.base import BaseController


class RGBLoadsController(BaseController[RGBLoad]):
    item_cls = RGBLoad
    vantage_types = (DGColorLoad, DDGColorLoad)
    status_types = (StatusType.LOAD,)

    def _update_object_state(self, vid: int, args: Sequence[str]) -> None:
        if vid in self:
            # RGBLoads only give us the load level in a "STATUS LOAD" status,
            # We could call "ADDSTATUS" for every vid, but ADDSTATUS replies are noisy
            # and have a limit of 64 per connection. Instead, we'll just call
            # RGBLoad.GetColor when an update is available.
            asyncio.create_task(self._fetch_object_state(vid))

    async def _fetch_object_state(self, vid: int) -> None:
        # Fetch initial state of a single Load.
        response = await self._vantage._hc_client.send_command(
            "INVOKE", f"{vid}", "RGBLoad.GetColor"
        )

        # INVOKE <vid> <color> RGBLoad.GetColor
        _, _, color, _ = shlex.split(response)

        # Unpack RGBW values from the 32-bit integer representation.
        r, g, b, w = struct.pack(">i", int(color))

        if vid in self:
            self[vid].rgb = (r, g, b)

    async def _fetch_initial_states(self) -> None:
        # Fetch initial state of all Loads.
        await asyncio.gather(*[self._fetch_object_state(load.id) for load in self])

    async def set_rgbw(
        self, id: int, red: int, green: int, blue: int, white: int
    ) -> None:
        """
        Set the color of an RGB load

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
        Set the color of an RGB load.

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
