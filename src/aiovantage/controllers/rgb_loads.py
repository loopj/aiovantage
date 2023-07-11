"""Controller holding and managing Vantage RGB loads."""

from typing import Any, Dict, List, Optional, Sequence, Tuple

from typing_extensions import override

from aiovantage.command_client.interfaces import (
    ColorTemperatureInterface,
    LoadInterface,
    RGBLoadInterface,
)
from aiovantage.config_client.objects import RGBLoadBase
from aiovantage.query import QuerySet

from .base import BaseController, State


class RGBLoadsController(
    BaseController[RGBLoadBase],
    LoadInterface,
    RGBLoadInterface,
    ColorTemperatureInterface,
):
    """Controller holding and managing Vantage RGB loads."""

    vantage_types = ("Vantage.DGColorLoad", "Vantage.DDGColorLoad")
    """The Vantage object types that this controller will fetch."""

    enhanced_log_status_methods = (
        "RGBLoad.GetHSL",
        "RGBLoad.GetRGB",
        "RGBLoad.GetRGBW",
        "ColorTemperature.Get",
        "Load.GetLevel",
    )
    """Which status methods this controller handles from the Enhanced Log."""

    def __post_init__(self) -> None:
        """Initialize the map for building colors."""
        self._temp_color_map: Dict[int, List[int]] = {}

    @override
    async def fetch_object_state(self, vid: int) -> State:
        """Fetch the state properties of an RGB load."""
        state: Dict[str, Any] = {
            "level": await LoadInterface.get_level(self, vid),
        }

        rgb_load: RGBLoadBase = self[vid]
        if rgb_load.is_rgb:
            state["hsl"] = await RGBLoadInterface.get_hsl(self, vid)
            state["rgb"] = await RGBLoadInterface.get_rgb(self, vid)
            state["rgbw"] = await RGBLoadInterface.get_rgbw(self, vid)

        if rgb_load.is_cct:
            state["color_temp"] = await ColorTemperatureInterface.get_color_temp(
                self, vid
            )

        return state

    @override
    def parse_object_update(self, vid: int, status: str, args: Sequence[str]) -> State:
        """Handle state changes for an RGB load."""
        rgb_load: RGBLoadBase = self[vid]
        if status == "Load.GetLevel":
            return {
                "level": LoadInterface.parse_get_level_status(args),
            }

        if status == "RGBLoad.GetHSL" and rgb_load.is_rgb:
            channel, value = RGBLoadInterface.parse_color_channel_status(args)
            if hsl := self._build_color_from_channels(vid, channel, value, 3):
                return {"hsl": hsl}
            return None

        if status == "RGBLoad.GetRGB" and rgb_load.is_rgb:
            channel, value = RGBLoadInterface.parse_color_channel_status(args)
            if rgb := self._build_color_from_channels(vid, channel, value, 3):
                return {"rgb": rgb}
            return None

        if status == "RGBLoad.GetRGBW" and rgb_load.is_rgb:
            channel, value = RGBLoadInterface.parse_color_channel_status(args)
            if rgbw := self._build_color_from_channels(vid, channel, value, 4):
                return {"rgbw": rgbw}
            return None

        if status == "ColorTemperature.Get" and rgb_load.is_cct:
            return {
                "color_temp": ColorTemperatureInterface.parse_get_status(args),
            }

        return None

    @property
    def is_on(self) -> QuerySet[RGBLoadBase]:
        """Return a queryset of all RGB loads that are turned on."""
        return self.filter(lambda load: load.is_on)

    @property
    def is_off(self) -> QuerySet[RGBLoadBase]:
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
