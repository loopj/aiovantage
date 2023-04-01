from dataclasses import dataclass, field
import logging
from collections.abc import Sequence
from typing import TYPE_CHECKING

from ..clients.hc import StatusType
from ..xml_dataclass import attr_field, element_field

if TYPE_CHECKING:
    from aiovantage import Vantage


@dataclass
class SystemObject:
    _logger: "logging.Logger" = field(init=False)
    _vantage: "Vantage | None" = field(init=False, default=None)

    id: int | None = attr_field(name="VID", default=None)
    name: str | None = element_field(name="Name", default=None)
    display_name: str | None = element_field(name="DName", default=None)

    def __post_init__(self) -> None:
        self._logger = logging.getLogger(__package__)

    @property
    def vantage(self) -> "Vantage":
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage

    def status_handler(self, type: StatusType, args: Sequence[str]) -> None:
        raise NotImplementedError("status_handler not implemented")