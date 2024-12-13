"""Base class for parent device objects."""

from dataclasses import dataclass

from .. import CustomDevice


@dataclass
class ParentDevice(CustomDevice):
    """Base class for parent device objects."""
