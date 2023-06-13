from aiovantage.command_client.interfaces import BlindInterface
from aiovantage.config_client.objects import Blind, BlindGroup
from aiovantage.query import QuerySet

from .base import BaseController


class BlindGroupsController(BaseController[BlindGroup], BlindInterface):
    # Fetch the following object types from Vantage
    vantage_types = ("BlindGroup", "Somfy.URTSI_2_Group_CHILD")

    def blinds(self, id: int) -> QuerySet[Blind]:
        """Return a queryset of all blinds in this blind group."""

        blind_group = self[id]
        if blind_group.blind_ids is not None:
            # Some blind groups have a list of blind ids, use that to filter
            return self._vantage.blinds.filter(
                lambda blind: blind.id in blind_group.blind_ids  # type: ignore
            )
        else:
            # Otherwise, use the parent_id to filter
            return self._vantage.blinds.filter(parent_id=blind_group.id)
