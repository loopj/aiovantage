"""Controller holding and managing Vantage blind groups."""

from aiovantage.controllers.base import BaseController
from aiovantage.controllers.blinds import BlindTypes
from aiovantage.models import (
    BlindGroup,
    ChildDevice,
    SomfyRS485GroupChild,
    SomfyURTSI2GroupChild,
)
from aiovantage.query import QuerySet

# The various "blind group" object types don't all inherit from the same base class,
# so for typing purposes we'll export a union of all the types.

BlindGroupTypes = BlindGroup | SomfyRS485GroupChild | SomfyURTSI2GroupChild
"""Types of objects that are considered 'blind groups'."""


class BlindGroupsController(BaseController[BlindGroupTypes]):
    """Controller holding and managing Vantage blind groups."""

    vantage_types = (
        "BlindGroup",
        "Somfy.RS-485_Group_CHILD",
        "Somfy.URTSI_2_Group_CHILD",
    )

    def blinds(self, vid: int) -> QuerySet[BlindTypes]:
        """Return a queryset of all blinds in this blind group."""
        blind_group = self[vid]
        if isinstance(blind_group, BlindGroup):

            def _filter1(blind: BlindTypes) -> bool:
                return blind.id in blind_group.blind_ids

            return self._vantage.blinds.filter(_filter1)

        # Otherwise, use the parent id to filter
        def _filter2(blind: BlindTypes) -> bool:
            if isinstance(blind, ChildDevice):
                return blind.parent.id == blind_group.id

            return False

        return self._vantage.blinds.filter(_filter2)
