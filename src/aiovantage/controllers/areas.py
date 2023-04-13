from typing import Optional

from aiovantage.controllers.base import BaseController
from aiovantage.aci_client.system_objects import Area


class AreasController(BaseController[Area]):
    item_cls = Area
    vantage_types = ("Area",)

    def root(self) -> Optional[Area]:
        """Return the root (top-most) area."""

        return self.get(area=0)
