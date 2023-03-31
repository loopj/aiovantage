import logging
from collections.abc import Sequence
from typing import TYPE_CHECKING

from ..clients.hc import StatusType
from .xml_model import XMLModel

if TYPE_CHECKING:
    from aiovantage import Vantage


class VantageObject(XMLModel):
    id: int
    _logger: "logging.Logger"
    _vantage: "Vantage | None" = None

    def __post_init__(self) -> None:
        self._logger = logging.getLogger(__package__)

    @property
    def vantage(self) -> "Vantage":
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage

    def status_handler(self, type: StatusType, args: Sequence[str]) -> None:
        raise NotImplementedError("status_handler not implemented")
