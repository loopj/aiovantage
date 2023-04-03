"""
This module provides a simple way to serialize and deserialize dataclasses to and
from XML.
"""

import xml.etree.ElementTree as ET
from dataclasses import Field, field, fields, is_dataclass
from typing import (
    Any,
    ClassVar,
    Optional,
    Protocol,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
)
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.formats.dataclass.parsers.handlers import XmlEventHandler
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig


def element_field(
    name: Optional[str] = None,
    **kwargs: Any,
) -> Any:
    """
    Return an object to identify a dataclass field, which will be populated from an
    element with the given name when deserializing from XML.
    """

    return field(metadata=dict(name=name, type="Element"), **kwargs)


def attr_field(name: Optional[str] = None, **kwargs: Any) -> Any:
    """
    Return an object to identify a dataclass field, which will be populated from an
    attribute with the given name when deserializing from XML.
    """

    return field(metadata=dict(name=name, type="Attribute"), **kwargs)


def _flatten_union(t: Any) -> Any:
    origin = get_origin(t)

    # We need to handle Union and UnionType separately because
    # get_origin(Union[blah]) is Union, get_origin(blah | None) is UnionType
    if origin is Union:
        return get_args(t)[0]
    else:
        return t

T = TypeVar("T")

def _parse_text(text: Optional[str], type: Type[T]) -> Any:
    if text is None:
        return None

    text = text.strip()
    if issubclass(type, bool):
        return text.lower() == "true"
    elif issubclass(type, (int, float)):
        return type(text)
    elif issubclass(type, str):
        return text

    return None


def _dump_text(value: Any, type: Any) -> str:
    if value is None:
        return ""

    if issubclass(type, bool):
        return str(value).lower()
    elif issubclass(type, (int, float)):
        return str(value)
    else:
        return str(value)


def _get_field_value(f: Field, el: ET.Element) -> Any:
    # Get the value from the XML element or attribute
    tag_type = f.metadata.get("type", "Element")
    tag_name = f.metadata.get("name", f.name)
    print(tag_name)
    if tag_type == "Element":
        tag_els = el.findall(tag_name)
        if tag_els:
            base_type = _flatten_union(f.type)
            type = get_origin(base_type) or base_type
            if issubclass(type, (list, tuple)):
                return type(
                    from_xml_el(tag_el, get_args(base_type)[0]) for tag_el in tag_els
                )
            else:
                return from_xml_el(tag_els[0], type)

    elif tag_type == "Attribute":
        field_value = el.get(tag_name)
        if field_value is not None:
            base_type = _flatten_union(f.type)
            type = get_origin(base_type) or base_type
            return _parse_text(field_value, type)


def _get_field_element(f: Field, obj: Any) -> Optional[ET.Element]:
    tag_type = f.metadata.get("type", "Element")
    tag_name = f.metadata.get("name", f.name)
    if tag_type == "Element":
        value = getattr(obj, f.name)
        if value is not None:
            base_type = _flatten_union(f.type)
            type = get_origin(base_type) or base_type
            if issubclass(type, (list, tuple)):
                el = ET.Element(tag_name)
                for item in value:
                    el.append(to_xml_el(item, tag_name))
                return el
            else:
                return to_xml_el(value, tag_name)

    elif tag_type == "Attribute":
        value = getattr(obj, f.name)
        if value is not None:
            base_type = _flatten_union(f.type)
            type = get_origin(base_type) or base_type
            el = ET.Element(tag_name)
            el.text = _dump_text(value, type)
            return el

    return None


class DataclassInstance(Protocol):
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]



# def from_xml_el(el: ET.Element, cls: Type[T]) -> T:
#     """Parse an XML element into a dataclass instance."""

#     print(ET.tostring(el))
#     print(cls, is_dataclass(cls))

#     if is_dataclass(cls):
#         kwargs = {}
#         for f in fields(cls):
#             print(f)
#             value = _get_field_value(f, el)
#             if value is not None:
#                 kwargs[f.name] = value

#         return cls(**kwargs)
#     else:
#         return _parse_text(el.text, cls)


# def to_xml_el(obj: T, root_name: str | None = None) -> ET.Element:
#     """Serialize a dataclass instance to an XML element."""

#     cls = obj.__class__
#     el = ET.Element(root_name or cls.__name__)
#     if is_dataclass(cls):
#         for f in fields(cls):
#             value = getattr(obj, f.name)
#             if value is not None:
#                 child_el = _get_field_element(f, obj)
#                 if child_el is not None:
#                     el.append(child_el)
#     else:
#         el.text = _dump_text(obj, cls)

#     return el

def from_xml_el(el: ET.Element, cls: Type[T]) -> T:
    """Parse an XML element into a dataclass instance."""

    config = ParserConfig(
        fail_on_unknown_properties=False,
        fail_on_unknown_attributes=False,
    )
    parser = XmlParser(handler=XmlEventHandler, config=config)
    return parser.parse(el, cls)


def to_xml_el(obj: T, root_name: Optional[str] = None) -> ET.Element:
    """Serialize a dataclass instance to an XML element."""

    # serializer = XmlSerializer()
    # serializer.render(obj)

    cls = obj.__class__
    el = ET.Element(root_name or cls.__name__)
    if is_dataclass(cls):
        for f in fields(cls):
            value = getattr(obj, f.name)
            if value is not None:
                child_el = _get_field_element(f, obj)
                if child_el is not None:
                    el.append(child_el)
    else:
        el.text = _dump_text(obj, cls)

    print(ET.tostring(el))

    return el