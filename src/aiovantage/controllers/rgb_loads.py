"""Controller holding and managing Vantage RGB loads."""

from typing import Any

from typing_extensions import override

from aiovantage.objects import VantageDDGColorLoad, VantageDGColorLoad
from aiovantage.query import QuerySet

from .base import BaseController

RGBLoadTypes = VantageDDGColorLoad | VantageDGColorLoad


class RGBLoadsController(BaseController[RGBLoadTypes]):
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
    async def fetch_object_state(self, obj: RGBLoadTypes) -> None:
        """Fetch the state properties of an RGB load."""
        state: dict[str, Any] = {}

        state["level"] = await obj.get_level()
        state["hsl"] = await obj.get_hsl_color()
        state["rgb"] = await obj.get_rgb_color()
        state["rgbw"] = await obj.get_rgbw_color()
        state["color_temp"] = await obj.get_color_temp()

        self.update_state(obj, state)

    @override
    def handle_interface_status(
        self, obj: RGBLoadTypes, method: str, result: str, *args: str
    ) -> None:
        """Handle object interface status messages from the event stream."""
        state: dict[str, Any] = {}

        if method == "Load.GetLevel":
            state["level"] = obj.parse_object_status(method, result, *args)

        elif method == "RGBLoad.GetHSL":
            if color := self._parse_color_channel_response(obj, method, result, *args):
                state["hsl"] = color

        elif method == "RGBLoad.GetRGB":
            if color := self._parse_color_channel_response(obj, method, result, *args):
                state["rgb"] = color

        elif method == "RGBLoad.GetRGBW":
            if color := self._parse_color_channel_response(obj, method, result, *args):
                state["rgbw"] = color

        elif method == "ColorTemperature.Get":
            state["color_temp"] = obj.parse_object_status(method, result, *args)

        else:
            return

        self.update_state(obj, state)

    @property
    def is_on(self) -> QuerySet[RGBLoadTypes]:
        """Return a queryset of all RGB loads that are turned on."""
        return self.filter(lambda load: load.is_on)

    @property
    def is_off(self) -> QuerySet[RGBLoadTypes]:
        """Return a queryset of all RGB loads that are turned off."""
        return self.filter(lambda load: not load.is_on)

    def _parse_color_channel_response(
        self, obj: RGBLoadTypes, method: str, result: str, *args: str
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
        self._temp_color_map.setdefault(obj.vid, num_channels * [0])
        self._temp_color_map[obj.vid][channel] = value

        # If we have all the channels, build and return the color
        if channel == num_channels - 1:
            color = tuple(self._temp_color_map[obj.vid])
            del self._temp_color_map[obj.vid]
            return color

        return None
