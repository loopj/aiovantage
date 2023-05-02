from dataclasses import dataclass

from xsdata.models.datatype import XmlDateTime

from ..xml_dataclass import xml_attribute, xml_element


@dataclass
class SystemObject:
    id: int = xml_attribute("VID")
    master_id: int = xml_attribute("Master")
    mtime: XmlDateTime = xml_attribute("MTime")
    name: str = xml_element("Name")
    model: str = xml_element("Model")
    note: str = xml_element("Note")
    display_name: str = xml_element("DName")
