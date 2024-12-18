"""Base class for all objects."""

from dataclasses import dataclass, field

from xsdata.models.datatype import XmlDateTime


@dataclass(kw_only=True)
class SystemObject:
    """Base class for all objects."""

    # MTime, DName, not available in 2.x firmware

    vid: int = field(metadata={"name": "VID", "type": "Attribute"})
    master: int = field(metadata={"type": "Attribute"})
    name: str
    model: str
    note: str
    m_time: XmlDateTime | None = field(default=None, metadata={"type": "Attribute"})
    d_name: str | None = None

    @property
    def id(self) -> int:
        """Return the Vantage ID of the object."""
        return self.vid

    @property
    def display_name(self) -> str:
        """Return the display name of the object."""
        return self.d_name or self.name

    @property
    def vantage_type(self) -> str:
        """Return the Vantage type of the object."""
        cls = type(self)
        cls_meta = getattr(cls, "Meta", None)
        return getattr(cls_meta, "name", cls.__qualname__)
