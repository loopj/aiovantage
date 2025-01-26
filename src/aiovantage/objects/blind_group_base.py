"""Blind group base class."""

from dataclasses import dataclass

from .blind_base import BlindBase


@dataclass(kw_only=True)
class BlindGroupBase(BlindBase):
    """Blind group base class."""
