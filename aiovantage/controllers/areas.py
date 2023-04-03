from typing import Optional

from ..models.area import Area
from .base import BaseController


class AreasController(BaseController[Area]):
    item_cls = Area
    vantage_types = ("Area",)

    def root(self) -> Optional[Area]:
        """Return the root (top-most) area."""
        return self.get(area_id=0)