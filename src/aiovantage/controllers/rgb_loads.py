"""Controller holding and managing Vantage RGB loads."""

from typing import Any, Dict, List, Optional, Tuple

from typing_extensions import override

from aiovantage.command_client.object_interfaces import (
    ColorTemperatureInterface,
    LoadInterface,
    RGBLoadInterface,
)
from aiovantage.command_client.object_interfaces.base import InterfaceResponse
from aiovantage.models import RGBLoadBase
from aiovantage.query import QuerySet

from .base import BaseController


class RGBLoadsController(
    BaseController[RGBLoadBase],
    LoadInterface,
    RGBLoadInterface,
    ColorTemperatureInterface,
):
    """Controller holding and managing Vantage RGB loads."""

    vantage_types = ("Vantage.DGColorLoad", "Vantage.DDGColorLoad")
    """The Vantage object types that this controller will fetch."""

    interface_status_types = (
        "Load.GetLevel",
        "RGBLoad.GetHSL",
        "RGBLoad.GetRGB",
        "RGBLoad.GetRGBW",
        "ColorTemperature.Get",
    )
    """Which object interface status messages this controller handles, if any."""

    def __post_init__(self) -> None:
        """Initialize the map for building colors."""
        self._temp_color_map: Dict[int, List[int]] = {}

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the state properties of an RGB load."""
        state: Dict[str, Any] = {
            "level": await LoadInterface.get_level(self, vid),
        }

        rgb_load: RGBLoadBase = self[vid]
        if rgb_load.is_rgb:
            state["hsl"] = await RGBLoadInterface.get_hsl_color(self, vid)
            state["rgb"] = await RGBLoadInterface.get_rgb_color(self, vid)
            state["rgbw"] = await RGBLoadInterface.get_rgbw_color(self, vid)

        if rgb_load.is_cct:
            state["color_temp"] = await ColorTemperatureInterface.get_color_temp(
                self, vid
            )

        self.update_state(vid, state)

    @override
    def handle_interface_status(self, status: InterfaceResponse) -> None:
        """Handle object interface status messages from the event stream."""
        rgb_load: RGBLoadBase = self[status.vid]
        state: Dict[str, Any] = {}

        if status.method == "Load.GetLevel":
            state["level"] = LoadInterface.parse_get_level_response(status)

        elif status.method == "RGBLoad.GetHSL" and rgb_load.is_rgb:
            channel, value = RGBLoadInterface.parse_get_hsl_response(status)
            if hsl := self._build_color(status.vid, channel, value, 3):
                state["hsl"] = hsl

        elif status.method == "RGBLoad.GetRGB" and rgb_load.is_rgb:
            channel, value = RGBLoadInterface.parse_get_rgb_response(status)
            if rgb := self._build_color(status.vid, channel, value, 3):
                state["rgb"] = rgb

        elif status.method == "RGBLoad.GetRGBW" and rgb_load.is_rgb:
            channel, value = RGBLoadInterface.parse_get_rgbw_response(status)
            if rgbw := self._build_color(status.vid, channel, value, 4):
                state["rgbw"] = rgbw

        elif status.method == "ColorTemperature.Get" and rgb_load.is_cct:
            state["color_temp"] = ColorTemperatureInterface.parse_get_response(status)

        self.update_state(status.vid, state)

    @property
    def is_on(self) -> QuerySet[RGBLoadBase]:
        """Return a queryset of all RGB loads that are turned on."""
        return self.filter(lambda load: load.is_on)

    @property
    def is_off(self) -> QuerySet[RGBLoadBase]:
        """Return a queryset of all RGB loads that are turned off."""
        return self.filter(lambda load: not load.is_on)

    def _build_color(
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
