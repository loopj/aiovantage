import xml.etree.ElementTree as ET
from typing import Optional


def get_element_text(el: ET.Element, tag: str) -> Optional[str]:
    child = el.find(tag)
    return child.text if child is not None else None


def get_element_int(el: ET.Element, tag: str) -> Optional[int]:
    text = get_element_text(el, tag)
    return int(text) if text is not None else None