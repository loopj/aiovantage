from typing import Any, Dict, List, Optional, Sequence, Tuple

from typing_extensions import override

from aiovantage.command_client.interfaces import (
    ColorTemperatureInterface,
    LoadInterface,
    RGBLoadInterface,
)
from aiovantage.config_client.objects import DDGColorLoad, DGColorLoad, RGBLoad

from .base import StatefulController


class RGBLoadsController(
    StatefulController[RGBLoad],
    LoadInterface,
    RGBLoadInterface,
    ColorTemperatureInterface,
):
    # Store objects managed by this controller as RGBLoad instances
    item_cls = RGBLoad

    # Fetch Vantage.DGColorLoad and Vantage.DDGColorLoad objects from Vantage
    vantage_types = (DGColorLoad, DDGColorLoad)

    # Subscribe to status updates from the event log for the following methods
    event_log_status_methods = (
        "RGBLoad.GetHSL",
        "RGBLoad.GetRGB",
        "RGBLoad.GetRGBW",
        "ColorTemperature.Get",
        "Load.GetLevel",
    )

    async def initialize(self) -> None:
        self._temp_color_map: Dict[int, List[int]] = {}
        return await super().initialize()

    @override
    async def fetch_object_state(self, id: int) -> None:
        # Fetch initial state of an RGBLoad.

        state: Dict[str, Any] = {}
        color_type = self[id].color_type

        # We care about HSL values for HSL, RGB, and RGBW loads, since color
        # information is lost in the rgb values when adjusting brightness/level.
        if color_type in (
            RGBLoad.ColorType.HSL,
            RGBLoad.ColorType.RGB,
            RGBLoad.ColorType.RGBW,
        ):
            state["hsl"] = await self.get_hsl(id)

        if color_type == RGBLoad.ColorType.RGB:
            state["rgb"] = await self.get_rgb(id)

        if color_type == RGBLoad.ColorType.RGBW:
            state["rgbw"] = await self.get_rgbw(id)

        if color_type == RGBLoad.ColorType.CCT:
            state["cct_temp"] = await self.get_color_temp(id)
            state["cct_level"] = await self.get_level(id)

        self.update_state(id, state)

    @override
    def handle_object_update(self, id: int, method: str, args: Sequence[str]) -> None:
        # Handle state changes for an RGBLoad.

        state: Dict[str, Any] = {}
        color_type = self[id].color_type

        if method == "RGBLoad.GetHSL":
            # <id> RGBLoad.GetHSL <value> <channel>

            # We care about HS values for RGB, and RGBW loads, since color information
            # is lost in the rgb values when adjusting brightness/level.
            if color_type in (
                RGBLoad.ColorType.HSL,
                RGBLoad.ColorType.RGB,
                RGBLoad.ColorType.RGBW,
            ):
                if hsl := self._build_color(id, args, num_channels=3):
                    state["hsl"] = RGBLoad.HSLValue(*hsl)

        elif method == "RGBLoad.GetRGB":
            # <id> RGBLoad.GetRGB <value> <channel>
            if color_type == RGBLoad.ColorType.RGB:
                if color := self._build_color(id, args, num_channels=3):
                    state["rgb"] = RGBLoad.RGBValue(*color)

        elif method == "RGBLoad.GetRGBW":
            # <id> RGBLoad.GetRGBW <value> <channel>
            if color_type == RGBLoad.ColorType.RGBW:
                if color := self._build_color(id, args, num_channels=4):
                    state["rgbw"] = RGBLoad.RGBWValue(*color)

        elif method == "ColorTemperature.Get":
            # <id> ColorTemperature.Get <temp>
            if color_type == RGBLoad.ColorType.CCT:
                state["cct_temp"] = int(args[0])

        elif method == "Load.GetLevel":
            # <id> Load.GetLevel <level (0-100000)>
            if color_type == RGBLoad.ColorType.CCT:
                state["cct_level"] = int(args[0]) / 1000

        self.update_state(id, state)

    def _build_color(
        self, id: int, args: Sequence[str], num_channels: int
    ) -> Optional[Tuple[int, ...]]:
        # Build a color from a series of channel values. We need to store partially
        # constructed colors in memory, since updates come separately for each channel.

        if id not in self._temp_color_map:
            self._temp_color_map[id] = num_channels * [0]

        # Extract the color and channel from the args
        channel = int(args[1])
        if channel < 0 or channel >= num_channels:
            return None
        self._temp_color_map[id][channel] = int(args[0])

        # If we have all the channels, build and return the color
        if channel == num_channels - 1:
            color = tuple(self._temp_color_map[id])
            del self._temp_color_map[id]
            return color

        return None
