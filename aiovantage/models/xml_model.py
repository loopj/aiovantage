import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, fields
from typing import Any, Dict, Type, TypeVar, Union, get_args, get_origin

def xml_tag(name: str, **kwargs: Any) -> Any:
    """Return a field that will be populated from the text of a tag with the given name when deserializing from XML."""
    return field(metadata={"xml_tag_name": name}, **kwargs)


def xml_attr(name: str, **kwargs: Any) -> Any:
    """Return a field that will be populated from an attribute with the given name when deserializing from XML."""
    return field(metadata={"xml_attr_name": name}, **kwargs)


def get_base_type(t: Any) -> Any:
    """Return the base type of a type, stripping off any Union (or Optional) types."""
    if get_origin(t) is Union:
        return get_args(t)[0]
    else:
        return t


T = TypeVar("T", bound="XMLModel")


@dataclass
class XMLModel:
    """Base class for models that can be deserialized from XML."""
    @classmethod
    def from_xml(cls: Type[T], el: ET.Element) -> T:
        """Deserialize an instance of this class from an XML element."""
        values: Dict[str, Any] = {}
        for f in fields(cls):
            field_value = None

            # Fetch the text from the element or attribute
            if "xml_attr_name" in f.metadata:
                field_value = el.get(f.metadata["xml_attr_name"])
            elif "xml_tag_name" in f.metadata:
                tag_el = el.find(f.metadata["xml_tag_name"])
                if tag_el is not None:
                    field_value = tag_el.text

            # Convert the value to the correct type
            if field_value is not None:
                type = get_base_type(f.type)
                values[f.name] = type(field_value.strip())

        return cls(**values)