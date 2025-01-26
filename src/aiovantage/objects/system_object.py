"""Base class for all objects."""

from dataclasses import dataclass, field

from xsdata.models.datatype import XmlDateTime


@dataclass(kw_only=True)
class SystemObject:
    """Base class for all objects."""

    vid: int = field(metadata={"name": "VID", "type": "Attribute"})
    master: int = field(metadata={"type": "Attribute"})
    name: str
    model: str
    note: str

    # Not available in 2.x firmware
    mtime: XmlDateTime | None = field(
        default=None, metadata={"name": "MTime", "type": "Attribute"}
    )
    dname: str | None = field(default=None, metadata={"name": "DName"})

    @property
    def id(self) -> int:
        """Return the ID of the object."""
        return self.vid

    @property
    def display_name(self) -> str:
        """Return the display name of the object."""
        return self.dname or self.name

    @classmethod
    def vantage_type(cls) -> str:
        """Return the Vantage type for this object."""
        cls_meta = getattr(cls, "Meta", None)
        return getattr(cls_meta, "name", cls.__qualname__)
