import logging
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from ..clients.hc import StatusType
from ..xml_dataclass import attr_field, element_field

if TYPE_CHECKING:
    from aiovantage import Vantage


@dataclass
class SystemObject:
    """Base class for all Vantage objects."""

    id: Optional[int] = attr_field(name="VID", default=None)
    name: Optional[str] = element_field(name="Name", default=None)
    display_name: Optional[str] = element_field(name="DName", default=None)

    def __post_init__(self) -> None:
        self._vantage: Optional["Vantage"] = None
        self._logger = logging.getLogger(__package__)

    @property
    def vantage(self) -> "Vantage":
        if self._vantage is None:
            raise Exception("Vantage client not set")

        return self._vantage

    def status_handler(self, type: StatusType, args: Sequence[str]) -> None:
        raise NotImplementedError("status_handler not implemented")
