"""ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""

from dataclasses import dataclass, field

from .system_object import SystemObject
from .types import Parent


@dataclass(kw_only=True)
class ModuleGen2(SystemObject):
    """ModuleGen2 object, eg. SDM12-EM, UDM08-EM."""

    @dataclass
    class LineFeed:
        name: str
        amperage: int = field(metadata={"type": "Attribute"})
        voltage: int = field(metadata={"type": "Attribute"})
        position: int = field(metadata={"type": "Attribute"})
        arc_fault: bool = field(metadata={"type": "Attribute"})

    parent: Parent
    line_feed_table: list[LineFeed] = field(
        default_factory=list,
        metadata={
            "name": "LineFeed",
            "wrapper": "LineFeedTable",
        },
    )
    quiet_mode: bool = False
    legacy_mode: bool = False
    alert: int
