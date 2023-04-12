from dataclasses import dataclass
from typing import Optional

from xsdata.models.datatype import XmlDateTime

from ..xml_dataclass import xml_attribute, xml_element


@dataclass
class SystemObject:
    id: int = xml_attribute("VID")
    master: Optional[int] = xml_attribute("Master", default=None)
    mtime: Optional[XmlDateTime] = xml_attribute("MTime", default=None)
    name: Optional[str] = xml_element("Name", default=None)
    model: Optional[str] = xml_element("Model", default=None)
    note: Optional[str] = xml_element("Note", default=None)
    display_name: Optional[str] = xml_element("DName", default=None)
