"""Base class for all objects."""

from dataclasses import dataclass

from xsdata.models.datatype import XmlDateTime

from aiovantage.config_client.xml_dataclass import xml_attribute, xml_element


@dataclass
class SystemObject:
    """Base class for all objects."""

    # TODO: Attribute name "id" doesn't conform to snake_case naming style
    id: int = xml_attribute("VID")
    master_id: int = xml_attribute("Master")
    mtime: XmlDateTime = xml_attribute("MTime")
    name: str = xml_element("Name")
    model: str = xml_element("Model")
    note: str = xml_element("Note")
    display_name: str = xml_element("DName")
