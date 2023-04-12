from dataclasses import field
from typing import Any


def xml_attribute(name: str, **kwargs: Any) -> Any:
    metadata = {"name": name, "type": "Attribute"}
    return field(metadata=metadata, **kwargs)

def xml_element(name: str, **kwargs: Any) -> Any:
    metadata = {"name": name, "type": "Element"}
    return field(metadata=metadata, **kwargs)