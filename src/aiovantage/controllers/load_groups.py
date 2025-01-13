"""Controller holding and managing Vantage load groups."""

from aiovantage.objects import LoadGroup

from .base import BaseController


class LoadGroupsController(BaseController[LoadGroup]):
    """Controller holding and managing Vantage load groups."""

    vantage_types = (LoadGroup,)
