from typing import Any, Dict, List, Optional, Sequence, Tuple

from typing_extensions import override

from aiovantage.command_client.interfaces import (
    ColorTemperatureInterface,
    LoadInterface,
    RGBLoadInterface,
)
from aiovantage.config_client.objects import RGBLoad
from aiovantage.query import QuerySet

from .base import StatefulController


class RGBLoadsController(
    StatefulController[RGBLoad],
    LoadInterface,
    RGBLoadInterface,
    ColorTemperatureInterface,
):
    # Fetch the following object types from Vantage
    vantage_types = ("Vantage.DGColorLoad", "Vantage.DDGColorLoad")

    # Subscribe to status updates from the event log for the following methods
    event_log_status = True
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

        rgb_load: RGBLoad = self[id]
        state: Dict[str, Any] = {}
        state["level"] = await LoadInterface.get_level(self, id)

        if rgb_load.is_rgb:
            state["hsl"] = await RGBLoadInterface.get_hsl(self, id)
            state["rgb"] = await RGBLoadInterface.get_rgb(self, id)
            state["rgbw"] = await RGBLoadInterface.get_rgbw(self, id)

        if rgb_load.is_cct:
            state["color_temp"] = await ColorTemperatureInterface.get_color_temp(
                self, id
            )

        self.update_state(id, state)

    @override
    def handle_object_update(self, id: int, method: str, args: Sequence[str]) -> None:
        # Handle state changes for an RGBLoad.

        rgb_load: RGBLoad = self[id]
        state: Dict[str, Any] = {}
        if method == "Load.GetLevel":
            state["level"] = LoadInterface.parse_get_level_status(args)

        elif method == "RGBLoad.GetHSL" and rgb_load.is_rgb:
            channel, value = RGBLoadInterface.parse_color_channel_status(args)
            if hsl := self._build_color_from_channels(id, channel, value, 3):
                state["hsl"] = hsl

        elif method == "RGBLoad.GetRGB" and rgb_load.is_rgb:
            channel, value = RGBLoadInterface.parse_color_channel_status(args)
            if rgb := self._build_color_from_channels(id, channel, value, 3):
                state["rgb"] = rgb

        elif method == "RGBLoad.GetRGBW" and rgb_load.is_rgb:
            channel, value = RGBLoadInterface.parse_color_channel_status(args)
            if rgbw := self._build_color_from_channels(id, channel, value, 4):
                state["rgbw"] = rgbw

        elif method == "ColorTemperature.Get" and rgb_load.is_cct:
            state["color_temp"] = ColorTemperatureInterface.parse_get_status(args)

        self.update_state(id, state)

    @property
    def on(self) -> QuerySet[RGBLoad]:
        """Return a queryset of all RGB loads that are turned on."""

        return self.filter(lambda load: load.is_on)

    @property
    def off(self) -> QuerySet[RGBLoad]:
        """Return a queryset of all RGB loads that are turned off."""

        return self.filter(lambda load: not load.is_on)

    def _build_color_from_channels(
        self, id: int, channel: int, value: int, num_channels: int
    ) -> Optional[Tuple[int, ...]]:
        # Build a color from a series of channel value events. We need to store
        # partially constructed colors in memory, since updates come separately for
        # each channel.

        # Ignore updates for channels we don't care about
        if channel < 0 or channel >= num_channels:
            return None

        # Store the channel value in the temp color map
        self._temp_color_map.setdefault(id, num_channels * [0])
        self._temp_color_map[id][channel] = value

        # If we have all the channels, build and return the color
        if channel == num_channels - 1:
            color = tuple(self._temp_color_map[id])
            del self._temp_color_map[id]
            return color

        return None
