"""Station bus object."""

from dataclasses import dataclass

from aiovantage.config_client.xml_dataclass import xml_element

from .system_object import SystemObject


@dataclass
class StationBus(SystemObject):
    """Station bus object."""

    parent_id: int = xml_element("Parent")
