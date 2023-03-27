import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, Type, TypeVar

from .utils import get_element_text

T = TypeVar("T", bound="Base")

if TYPE_CHECKING:
    from aiovantage import Vantage


@dataclass
class Base:
    _vantage: "Vantage" = field(init=False, repr=False, compare=False)
    id: int
    name: Optional[str] = None
    display_name: Optional[str] = None

    @classmethod
    def from_xml(cls: Type[T], el: ET.Element) -> T:
        obj = cls(int(el.attrib["VID"]))
        obj.name = get_element_text(el, "Name")
        obj.display_name = get_element_text(el, "DName")
        return obj
