from typing import Optional

from aiovantage.config_client.objects import Area
from aiovantage.controllers.base import BaseController


class AreasController(BaseController[Area]):
    # Store objects managed by this controller as Area instances
    item_cls = Area

    # Fetch Area objects from Vantage
    vantage_types = (Area, )

    @property
    def root(self) -> Optional[Area]:
        """Return the root (top-most) area."""

        return self.get(area_id=0)
