"""Controller holding and managing Vantage RGB loads."""

from typing import Any

from typing_extensions import override

from aiovantage.object_interfaces import (
    ColorTemperatureInterface,
    LoadInterface,
    RGBLoadInterface,
)
from aiovantage.objects import VantageDDGColorLoad, VantageDGColorLoad
from aiovantage.query import QuerySet

from .base import BaseController

# The various "rgb load" object types don't all inherit from the same base class,
# so for typing purposes we'll use a union of all the types.
RGBLoadTypes = VantageDGColorLoad | VantageDDGColorLoad


class RGBLoadsController(BaseController[RGBLoadTypes]):
    """Controller holding and managing Vantage RGB loads."""

    vantage_types = (VantageDGColorLoad, VantageDDGColorLoad)
    interface_status_types = (
        "Load.GetLevel",
        "RGBLoad.GetHSL",
        "RGBLoad.GetRGB",
        "RGBLoad.GetRGBW",
        "ColorTemperature.Get",
    )

    def __post_init__(self) -> None:
        """Initialize the map for building colors."""
        self._temp_color_map: dict[int, list[int]] = {}

    @override
    async def fetch_object_state(self, obj: RGBLoadTypes) -> None:
        """Fetch the state properties of an RGB load."""
        state: dict[str, Any] = {
            "level": await obj.get_level(),
            "hsl": await obj.get_hsl_color(),
            "rgb": await obj.get_rgb_color(),
            "rgbw": await obj.get_rgbw_color(),
            "color_temp": await obj.get_temperature(),
        }

        self.update_state(obj.vid, state)

    @override
    def handle_interface_status(
        self, vid: int, method: str, result: str, *args: str
    ) -> None:
        """Handle object interface status messages from the event stream."""
        state: dict[str, Any] = {}

        if method == "Load.GetLevel":
            state["level"] = LoadInterface.parse_response(method, result, *args)

        elif method == "RGBLoad.GetHSL":
            if color := self._parse_color_channel_response(vid, method, result, *args):
                state["hsl"] = color

        elif method == "RGBLoad.GetRGB":
            if color := self._parse_color_channel_response(vid, method, result, *args):
                state["rgb"] = color

        elif method == "RGBLoad.GetRGBW":
            if color := self._parse_color_channel_response(vid, method, result, *args):
                state["rgbw"] = color

        elif method == "ColorTemperature.Get":
            state["color_temp"] = ColorTemperatureInterface.parse_response(
                method, result, *args
            )

        else:
            return

        self.update_state(vid, state)

    @property
    def is_on(self) -> QuerySet[RGBLoadTypes]:
        """Return a queryset of all RGB loads that are turned on."""
        return self.filter(lambda load: load.is_on)

    @property
    def is_off(self) -> QuerySet[RGBLoadTypes]:
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
        response = RGBLoadInterface.parse_response(
            method, result, *args, as_type=RGBLoadInterface.ColorChannelResponse
        )

        # Ignore updates for channels we don't care about
        if response.channel < 0 or response.channel >= num_channels:
            return None

        # Store the channel value in the temp color map
        self._temp_color_map.setdefault(vid, num_channels * [0])
        self._temp_color_map[vid][response.channel] = response.value

        # If we have all the channels, build and return the color
        if response.channel == num_channels - 1:
            color = tuple(self._temp_color_map[vid])
            del self._temp_color_map[vid]
            return color

        return None
