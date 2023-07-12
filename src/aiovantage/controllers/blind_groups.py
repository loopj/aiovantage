"""Controller holding and managing Vantage blind groups."""

from aiovantage.command_client.interfaces import BlindInterface
from aiovantage.models import BlindBase, BlindGroup, BlindGroupBase
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
            # BlindGroup objects have a list of blind ids, so use that to filter
            def _filter(blind: BlindBase) -> bool:
                return blind.id in blind_group.blind_ids

            return self._vantage.blinds.filter(_filter)

        # Otherwise, use the parent id to filter
        return self._vantage.blinds.filter(parent_id=blind_group.id)
