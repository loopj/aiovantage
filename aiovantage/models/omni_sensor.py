from dataclasses import dataclass
from typing import Optional

from .base import Base


@dataclass
class OmniSensor(Base):
    id: int
    name: Optional[str] = None
    display_name: Optional[str] = None
    _level: Optional[float] = None