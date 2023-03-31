import logging
from typing import TYPE_CHECKING

from .xml_model import XMLModel

if TYPE_CHECKING:
    from aiovantage import Vantage


class VantageObject(XMLModel):
    id: int
    _logger: "logging.Logger"
    _vantage: "Vantage | None" = None

    def __post_init__(self) -> None:
        self._logger = logging.getLogger(__package__)

    def status_handler(self, args: list[str]) -> None:
        pass
