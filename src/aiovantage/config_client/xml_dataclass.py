"""Helper functions for XML dataclasses."""

from dataclasses import field
from typing import Any, Type


def xml_attribute(name: str, **kwargs: Any) -> Any:
    """Create a dataclass field for an XML attribute."""
    metadata = {}
    metadata.update(kwargs.pop("metadata", {}))
    metadata.update({"name": name, "type": "Attribute"})

    return field(metadata=metadata, **kwargs)


def xml_element(name: str, **kwargs: Any) -> Any:
    """Create a dataclass field for an XML element."""
    metadata = {}
    metadata.update(kwargs.pop("metadata", {}))
    metadata.update({"name": name, "type": "Element"})

    if "wrapper" in kwargs:
        metadata.update({"wrapper": kwargs.pop("wrapper")})

    return field(metadata=metadata, **kwargs)


def xml_text(**kwargs: Any) -> Any:
    """Create a dataclass field for an XML text node."""
    metadata = {}
    metadata.update(kwargs.pop("metadata", {}))
    metadata.update({"type": "Text"})

    return field(metadata=metadata, **kwargs)


def xml_tag_from_class(cls: Type[Any]) -> str:
    """Get the XML tag name for a class."""

    # TODO: Cannot access member "Meta" for type "type" Member "Meta" is unknown
    meta = cls.Meta if "Meta" in cls.__dict__ else None
    name = getattr(meta, "name", cls.__qualname__)

    return name
