"""Configuration interface (IConfiguration) method definitions."""

from .close_filter import CloseFilter
from .get_filter_results import GetFilterResults
from .get_object import GetObject
from .open_filter import OpenFilter

__all__ = [
    "CloseFilter",
    "GetFilterResults",
    "GetObject",
    "OpenFilter",
]
