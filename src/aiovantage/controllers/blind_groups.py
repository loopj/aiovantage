"""Controller holding and managing Vantage blind groups."""

from aiovantage.objects import (
    BlindGroup,
    ChildDevice,
    SomfyRS485GroupChild,
    SomfyURTSI2GroupChild,
)
from aiovantage.query import QuerySet

from .base import BaseController
from .blinds import BlindTypes

# The various "blind group" object types don't all inherit from the same base class,
# so for typing purposes we'll use a union of all the types.
BlindGroupTypes = BlindGroup | SomfyRS485GroupChild | SomfyURTSI2GroupChild


class BlindGroupsController(BaseController[BlindGroupTypes]):
    """Controller holding and managing Vantage blind groups."""

    vantage_types = (BlindGroup, SomfyRS485GroupChild, SomfyURTSI2GroupChild)

    def blinds(self, vid: int) -> QuerySet[BlindTypes]:
        """Return a queryset of all blinds in this blind group."""
        blind_group = self[vid]
        if isinstance(blind_group, BlindGroup):

            def _filter1(blind: BlindTypes) -> bool:
                return blind.vid in blind_group.blind_table

            return self._vantage.blinds.filter(_filter1)

        # Otherwise, use the parent id to filter
        def _filter2(blind: BlindTypes) -> bool:
            if isinstance(blind, ChildDevice):
                return blind.parent.vid == blind_group.vid

            return False

        return self._vantage.blinds.filter(_filter2)
