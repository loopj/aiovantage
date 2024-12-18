"""Controller holding and managing Vantage blind groups."""

from aiovantage.models import BlindBase, BlindGroup, BlindGroupBase, ChildDevice
from aiovantage.object_interfaces import BlindInterface
from aiovantage.query import QuerySet

from .base import BaseController


class BlindGroupsController(BaseController[BlindGroupBase], BlindInterface):
    """Controller holding and managing Vantage blind groups."""

    vantage_types = (
        "BlindGroup",
        "Somfy.RS-485_Group_CHILD",
        "Somfy.URTSI_2_Group_CHILD",
    )
    """The Vantage object types that this controller will fetch."""

    def blinds(self, vid: int) -> QuerySet[BlindBase]:
        """Return a queryset of all blinds in this blind group."""
        blind_group = self[vid]
        if isinstance(blind_group, BlindGroup):

            def _filter1(blind: BlindBase) -> bool:
                return blind.id in blind_group.blind_ids

            return self._vantage.blinds.filter(_filter1)

        # Otherwise, use the parent id to filter
        def _filter2(blind: BlindBase) -> bool:
            if isinstance(blind, ChildDevice):
                return blind.parent.id == blind_group.id

            return False

        return self._vantage.blinds.filter(_filter2)
