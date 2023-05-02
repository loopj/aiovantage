from typing import Optional

from aiovantage.config_client.system_objects import Area
from aiovantage.vantage.controllers.base import BaseController


class AreasController(BaseController[Area]):
    item_cls = Area
    vantage_types = (Area,)

    @property
    def root(self) -> Optional[Area]:
        """Return the root (top-most) area."""

        return self.get(area_id=0)
