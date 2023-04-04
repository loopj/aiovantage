import logging
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional

from aiovantage.clients.hc import StatusType

if TYPE_CHECKING:
    from aiovantage import Vantage


@dataclass
class SystemObject:
    """Base class for all Vantage objects."""

    id: int = field(
        metadata=dict(
            type="Attribute",
            name="VID",
        ),
    )

    name: Optional[str] = field(
        default=None,
        metadata=dict(
            type="Element",
            name="Name",
        ),
    )

    display_name: Optional[str] = field(
        default=None,
        metadata=dict(
            type="Element",
            name="DName",
        ),
    )

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
