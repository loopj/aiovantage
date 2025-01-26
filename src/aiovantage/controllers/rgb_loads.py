"""Controller holding and managing Vantage RGB loads."""

from typing import Any

from typing_extensions import override

from aiovantage.object_interfaces import (
    ColorTemperatureInterface,
    LoadInterface,
    RGBLoadInterface,
)
from aiovantage.objects import RGBLoadBase
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
        self._temp_color_map: dict[int, list[int]] = {}

    @override
    async def fetch_object_state(self, vid: int) -> None:
        """Fetch the state properties of an RGB load."""
        state: dict[str, Any] = {
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
    def handle_interface_status(
        self, vid: int, method: str, result: str, *args: str
    ) -> None:
        """Handle object interface status messages from the event stream."""
        rgb_load: RGBLoadBase = self[vid]
        state: dict[str, Any] = {}

        if method == "Load.GetLevel":
            state["level"] = self.parse_object_status(method, result, *args)

        elif method == "RGBLoad.GetHSL" and rgb_load.is_rgb:
            if color := self._parse_color_channel_response(vid, method, result, *args):
                state["hsl"] = color

        elif method == "RGBLoad.GetRGB" and rgb_load.is_rgb:
            if color := self._parse_color_channel_response(vid, method, result, *args):
                state["rgb"] = color

        elif method == "RGBLoad.GetRGBW" and rgb_load.is_rgb:
            if color := self._parse_color_channel_response(vid, method, result, *args):
                state["rgbw"] = color

        elif method == "ColorTemperature.Get" and rgb_load.is_cct:
            state["color_temp"] = self.parse_object_status(method, result, *args)

        else:
            return

        self.update_state(vid, state)

    @property
    def is_on(self) -> QuerySet[RGBLoadBase]:
        """Return a queryset of all RGB loads that are turned on."""
        return self.filter(lambda load: load.is_on)

    @property
    def is_off(self) -> QuerySet[RGBLoadBase]:
        """Return a queryset of all RGB loads that are turned off."""
        return self.filter(lambda load: not load.is_on)

    def _parse_color_channel_response(
        self, vid: int, method: str, result: str, *args: str
    ) -> tuple[int, ...] | None:
        # Build a color from a series of channel responses. We need to store
        # partially constructed colors in memory, since updates come separately for
        # each channel.

        # Determine how many channels we need to build a color
        if method in ("RGBLoad.GetHSL", "RGBLoad.GetRGB"):
            num_channels = 3
        elif method == "RGBLoad.GetRGBW":
            num_channels = 4
        else:
            raise ValueError(f"Unsupported color channel method {method}")

        # Parse the response
        channel = int(args[0])
        value = int(result)

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
