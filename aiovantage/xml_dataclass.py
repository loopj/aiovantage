"""
This module provides a simple way to serialize and deserialize dataclasses to and
from XML.
"""

import xml.etree.ElementTree as ET
from dataclasses import Field, field, fields, is_dataclass
from types import UnionType
from typing import (
    Any,
    Callable,
    ClassVar,
    Protocol,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
)


def element_field(
    name: str | None = None,
    factory: Callable[[ET.Element, Any], Any] | None = None,
    **kwargs: Any,
) -> Any:
    """
    Return an object to identify a dataclass field, which will be populated from an
    element with the given name when deserializing from XML.
    """

    return field(
        metadata={
            "xml_dataclass": {"source": "element", "name": name, "factory": factory}
        },
        **kwargs,
    )


def attr_field(name: str | None = None, **kwargs: Any) -> Any:
    """
    Return an object to identify a dataclass field, which will be populated from an
    attribute with the given name when deserializing from XML.
    """

    return field(metadata={"xml_dataclass": {"source": "attr", "name": name}}, **kwargs)


def text_field(**kwargs: Any) -> Any:
    """
    Return an object to identify a dataclass field, which will be populated from the
    text of the element when deserializing from XML.
    """

    return field(metadata={"xml_dataclass": {"source": "text"}}, **kwargs)


def _flatten_union(t: Any) -> Any:
    origin = get_origin(t)

    # We need to handle Union and UnionType separately because
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
    if is_dataclass(type):
        return from_xml_el(el, type)
    else:
        return _parse_text(el.text, type)


def _dump_text(value: Any, type: Any) -> str:
    if value is None:
        return ""

    if issubclass(type, bool):
        return str(value).lower()
    elif issubclass(type, (int, float)):
        return str(value)
    else:
        return str(value)


def _dump_element(name: str, value: Any, type: Any) -> ET.Element:
    el = ET.Element(name)
    if is_dataclass(type):
        el.append(to_xml_el(value))
    else:
        el.text = _dump_text(value, type)

    return el


def _get_field_value(f: Field, el: ET.Element) -> Any:
    settings = f.metadata.get("xml_dataclass", {})
    if "source" not in settings:
        return None

    # Get the value from the XML element or attribute
    if settings["source"] == "element":
        tag_els = el.findall(settings.get("name") or f.name)
        if tag_els:
            base_type = _flatten_union(f.type)
            type = get_origin(base_type) or base_type
            factory = settings.get("factory") or _parse_element
            if issubclass(type, (list, tuple)):
                return type(
                    factory(tag_el, get_args(base_type)[0]) for tag_el in tag_els
                )
            else:
                return factory(tag_els[0], type)

    elif settings["source"] == "attr":
        field_value = el.get(settings.get("name") or f.name)
        if field_value is not None:
            base_type = _flatten_union(f.type)
            type = get_origin(base_type) or base_type
            if issubclass(type, (list, tuple)):
                raise TypeError("XML Attributes cannot be lists")
            else:
                return _parse_text(field_value, type)

    elif settings["source"] == "text":
        return _parse_text(el.text, f.type)


class DataclassInstance(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


T = TypeVar("T", bound=DataclassInstance)


def from_xml_el(el: ET.Element, cls: Type[T]) -> T:
    """Parse an XML element into a dataclass instance."""

    kwargs = {}
    for f in fields(cls):
        value = _get_field_value(f, el)
        if value is not None:
            kwargs[f.name] = value

    return cls(**kwargs)


def from_xml(xml: str, cls: Type[T]) -> T:
    """Parse an XML string into a dataclass instance."""

    el = ET.fromstring(xml)
    return from_xml_el(el, cls)


def to_xml_el(obj: T, root_name: str | None = None) -> ET.Element:
    """Serialize a dataclass instance to an XML element."""

    cls = obj.__class__
    el = ET.Element(root_name or cls.__name__)
    for f in fields(cls):
        value = getattr(obj, f.name)
        if value is not None:
            settings = f.metadata.get("xml_dataclass", {})
            if "source" not in settings:
                continue

            if settings["source"] == "element":
                if is_dataclass(f.type):
                    child_el = to_xml_el(value)
                    el.append(child_el)
                else:
                    base_type = _flatten_union(f.type)
                    type = get_origin(base_type) or base_type
                    if issubclass(type, (list, tuple)):
                        for item in value:
                            child_el = ET.Element(settings.get("name") or f.name)
                            child_el.text = _dump_text(item, type)
                            el.append(child_el)
                    else:
                        child_el = ET.Element(settings.get("name") or f.name)
                        child_el.text = _dump_text(value, type)
                        el.append(child_el)

            elif settings["source"] == "attr":
                base_type = _flatten_union(f.type)
                type = get_origin(base_type) or base_type
                el.set(settings.get("name") or f.name, _dump_text(value, type))

            elif settings["source"] == "text":
                el.text = str(value)

    return el


def to_xml(obj: T) -> str:
    """Serialize a dataclass instance to an XML string."""

    el = to_xml_el(obj)
    return ET.tostring(el, encoding="unicode")