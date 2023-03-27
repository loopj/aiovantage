from dataclasses import dataclass
from typing import Optional

from .base import Base


@dataclass
class OmniSensor(Base):
    _level: Optional[float] = None