from dataclasses import dataclass
from typing import Optional

from .base import Base


@dataclass
class Variable(Base):
    id: int
    name: Optional[str] = None
    display_name: Optional[str] = None