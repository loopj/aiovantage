import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, fields, Field
from typing import Any, Type, TypeVar, Union, get_args, get_origin
from types import UnionType


def element(alias: str | None = None, **kwargs: Any) -> Any:
    """Return a field that will be populated from the text of a tag with the given name when deserializing from XML."""
    return field(
        metadata={"xml_dataclass": {"source": "element", "alias": alias}}, **kwargs
    )


def attr(alias: str | None = None, **kwargs: Any) -> Any:
    """Return a field that will be populated from an attribute with the given name when deserializing from XML."""
    return field(
        metadata={"xml_dataclass": {"source": "attr", "alias": alias}}, **kwargs
    )


def _flatten_union(t: Any) -> Any:
    """Return the first type argument of a Union, or the type itself if it's not a Union."""
    origin = get_origin(t)

    # get_origin(Union[blah]) is Union, get_origin(blah | None) is UnionType
    if origin is Union or origin is UnionType:
        return get_args(t)[0]
    else:
        return t


def _parse_text(text: str | None, type: Any) -> Any:
    if text is None:
        return None

    text = text.strip()
    if issubclass(type, bool):
        return text.lower() == "true"
    elif issubclass(type, (int, float)):
        return type(text.strip())
    else:
        return text


def _parse_element(el: ET.Element, type: Any) -> Any:
    if issubclass(type, XMLModel):
        return type.from_xml_el(el)
    else:
        return _parse_text(el.text, type)


def _get_field_value(f: Field, el: ET.Element) -> Any:
    settings = f.metadata.get("xml_dataclass", {})
    if "source" not in settings:
        return None

    # Get the value from the XML element or attribute
    if settings["source"] == "element":
        tag_els = el.findall(settings.get("alias") or f.name)
        if tag_els:
            base_type = _flatten_union(f.type)
            type = get_origin(base_type) or base_type
            if issubclass(type, (list, tuple)):
                return type(
                    _parse_element(tag_el, get_args(base_type)[0]) for tag_el in tag_els
                )
            else:
                return _parse_element(tag_els[0], type)

    elif settings["source"] == "attr":
        field_value = el.get(settings.get("alias") or f.name)
        if field_value is not None:
            base_type = _flatten_union(f.type)
            type = get_origin(base_type) or base_type
            if issubclass(type, (list, tuple)):
                raise TypeError("XML Attributes cannot be lists")
            else:
                return _parse_text(field_value, type)


T = TypeVar("T", bound="XMLModel")


@dataclass
class XMLModel:
    """Base class for models that can be deserialized from XML."""

    @classmethod
    def from_xml(cls: Type[T], xml: str) -> T:
        """Deserialize an instance of this class from XML."""
        el = ET.fromstring(xml)
        return cls.from_xml_el(el)

    @classmethod
    def from_xml_el(cls: Type[T], el: ET.Element) -> T:
        """Deserialize an instance of this class from an XML element."""
        kwargs = {}
        for f in fields(cls):
            value = _get_field_value(f, el)
            if value is not None:
                kwargs[f.name] = value

        return cls(**kwargs)