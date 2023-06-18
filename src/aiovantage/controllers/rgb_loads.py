"""Controller holding and managing Vantage RGB loads."""

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
    """Controller holding and managing Vantage RGB loads."""

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

    def __post_init__(self) -> None:
        """Post initialization hook."""
        self._temp_color_map: Dict[int, List[int]] = {}

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the initial state of an RGB load."""

        state: Dict[str, Any] = {
            "level": await LoadInterface.get_level(self, vid),
        }

        rgb_load: RGBLoad = self[vid]
        if rgb_load.is_rgb:
            state["hsl"] = await RGBLoadInterface.get_hsl(self, vid)
            state["rgb"] = await RGBLoadInterface.get_rgb(self, vid)
            state["rgbw"] = await RGBLoadInterface.get_rgbw(self, vid)

        if rgb_load.is_cct:
            state["color_temp"] = await ColorTemperatureInterface.get_color_temp(
                self, vid
            )

        self.update_state(vid, state)

    @override
    def handle_object_update(self, vid: int, status: str, args: Sequence[str]) -> None:
        """Handle state changes for an RGB load."""

        rgb_load: RGBLoad = self[vid]
        state: Dict[str, Any] = {}
        if status == "Load.GetLevel":
            state["level"] = LoadInterface.parse_get_level_status(args)

        elif status == "RGBLoad.GetHSL" and rgb_load.is_rgb:
            channel, value = RGBLoadInterface.parse_color_channel_status(args)
            if hsl := self._build_color_from_channels(vid, channel, value, 3):
                state["hsl"] = hsl

        elif status == "RGBLoad.GetRGB" and rgb_load.is_rgb:
            channel, value = RGBLoadInterface.parse_color_channel_status(args)
            if rgb := self._build_color_from_channels(vid, channel, value, 3):
                state["rgb"] = rgb

        elif status == "RGBLoad.GetRGBW" and rgb_load.is_rgb:
            channel, value = RGBLoadInterface.parse_color_channel_status(args)
            if rgbw := self._build_color_from_channels(vid, channel, value, 4):
                state["rgbw"] = rgbw

        elif status == "ColorTemperature.Get" and rgb_load.is_cct:
            state["color_temp"] = ColorTemperatureInterface.parse_get_status(args)

        self.update_state(vid, state)

    @property
    def on(self) -> QuerySet[RGBLoad]:
        """Return a queryset of all RGB loads that are turned on."""

        return self.filter(lambda load: load.is_on)

    @property
    def off(self) -> QuerySet[RGBLoad]:
        """Return a queryset of all RGB loads that are turned off."""

        return self.filter(lambda load: not load.is_on)

    def _build_color_from_channels(
        self, vid: int, channel: int, value: int, num_channels: int
    ) -> Optional[Tuple[int, ...]]:
        # Build a color from a series of channel value events. We need to store
        # partially constructed colors in memory, since updates come separately for
        # each channel.

        # Ignore updates for channels we don't care about
        if channel < 0 or channel >= num_channels:
            return None

        # Store the channel value in the temp color map
        self._temp_color_map.setdefault(vid, num_channels * [0])
        self._temp_color_map[vid][channel] = value

        # If we have all the channels, build and return the color
        if channel == num_channels - 1:
            color = tuple(self._temp_color_map[vid])
            del self._temp_color_map[vid]
            return color

        return None
