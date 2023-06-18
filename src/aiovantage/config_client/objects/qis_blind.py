"""QIS blind object."""

from dataclasses import dataclass

from .blind import Blind


@dataclass
class QISBlind(Blind):
    """QIS blind object."""
