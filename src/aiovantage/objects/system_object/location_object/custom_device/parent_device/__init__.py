"""Base class for parent device objects."""

from dataclasses import dataclass

from .. import CustomDevice


@dataclass(kw_only=True)
class ParentDevice(CustomDevice):
    """Base class for parent device objects."""
