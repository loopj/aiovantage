from dataclasses import field
from typing import Any, Type


def xml_attribute(name: str, **kwargs: Any) -> Any:
    metadata = {}
    metadata.update(kwargs.pop("metadata", {}))
    metadata.update({"name": name, "type": "Attribute"})

    return field(metadata=metadata, **kwargs)


def xml_element(name: str, **kwargs: Any) -> Any:
    metadata = {}
    metadata.update(kwargs.pop("metadata", {}))
    metadata.update({"name": name, "type": "Element"})

    return field(metadata=metadata, **kwargs)


def xml_text(**kwargs: Any) -> Any:
    metadata = {}
    metadata.update(kwargs.pop("metadata", {}))
    metadata.update({"type": "Text"})

    return field(metadata=metadata, **kwargs)


def xml_tag_from_class(cls: Type[Any]) -> str:
    """Get the XML tag name for a class."""

    meta = cls.Meta if "Meta" in cls.__dict__ else None
    name = getattr(meta, "name", cls.__qualname__)

    return name
