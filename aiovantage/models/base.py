from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiovantage import Vantage


@dataclass
class Base:
    id: int
    _vantage: "Vantage" = field(init=False, repr=False, compare=False)