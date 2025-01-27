"""Module object."""

from dataclasses import dataclass, field

from .system_object import SystemObject
from .types import Parent


@dataclass(kw_only=True)
class Module(SystemObject):
    """Module object."""

    @dataclass
    class LineFeed:
        name: str
        amperage: int = field(metadata={"type": "Attribute"})
        voltage: int = field(metadata={"type": "Attribute"})
        position: int = field(metadata={"type": "Attribute"})

    parent: Parent
    line_feed_table: list[LineFeed] = field(
        default_factory=list,
        metadata={
            "name": "LineFeed",
            "wrapper": "LineFeedTable",
        },
    )
    join1: bool
    join2: bool
    join3: bool
    join4: bool
    quiet_mode: bool
