from dataclasses import dataclass
from typing import Optional

@dataclass
class VantageObject:
    id: int = None
    name: Optional[str] = None
    display_name: Optional[str] = None

    @classmethod
    def from_xml(cls, el):
        obj = cls()
        obj.id = int(el.attrib["VID"])
        obj.name = el.find("Name").text
        obj.display_name = el.find("DName").text
        return obj

@dataclass
class Area(VantageObject):
    parent_id: Optional[int] = None

    @classmethod
    def from_xml(cls, el):
        obj = super().from_xml(el)
        obj.parent_id = int(el.find("Area").text)
        return obj

    @property
    def parent(self):
        return self._vantage.areas.get(self.parent_id)

    @property
    def lineage(self):
        lineage = [self]
        area = self
        while area.parent:
            lineage.append(area.parent)
            area = area.parent

        return lineage

    @property
    def areas(self):
        return self._vantage.areas.filter(lambda obj: obj.parent_id == self.id)

    @property
    def stations(self):
        return self._vantage.stations.filter(lambda obj: obj.area_id == self.id)

    @property
    def loads(self):
        return self._vantage.loads.filter(lambda obj: obj.area_id == self.id)

    @property
    def dry_contacts(self):
        return self._vantage.dry_contacts.filter(lambda obj: obj.area_id == self.id)

@dataclass
class Load(VantageObject):
    load_type: Optional[str] = None
    area_id: Optional[int] = None
    level: Optional[float] = None

    @classmethod
    def from_xml(cls, el):
        obj = super().from_xml(el)
        obj.load_type = el.find("LoadType").text
        obj.area_id = int(el.find("Area").text)
        return obj

    @property
    def area(self):
        return self._vantage.areas.get(self.area_id)

@dataclass
class Station(VantageObject):
    area_id: Optional[int] = None
    bus_id: Optional[int] = None

    @classmethod
    def from_xml(cls, el):
        obj = super().from_xml(el)
        obj.area_id = int(el.find("Area").text)
        obj.bus_id = int(el.find("Bus").text)
        return obj

    @property
    def area(self):
        return self._vantage.areas.get(self.area_id)

    @property
    def buttons(self):
        return self._vantage.buttons.filter(lambda obj: obj.station_id == self.id)

    @property
    def dry_contacts(self):
        return self._vantage.dry_contacts.filter(lambda obj: obj.station_id == self.id)

@dataclass
class Button(VantageObject):
    text: Optional[str] = None
    station_id: Optional[int] = None

    @classmethod
    def from_xml(cls, el):
        obj = super().from_xml(el)
        obj.station_id = int(el.find("Parent").text)
        obj.text = el.find("Text1").text
        return obj

    @property
    def station(self):
        return self._vantage.stations.get(self.station_id)

@dataclass
class DryContact(VantageObject):
    area_id: Optional[int] = None
    station_id: Optional[int] = None

    @classmethod
    def from_xml(cls, el):
        obj = super().from_xml(el)
        obj.station_id = int(el.find("Parent").text)
        obj.area_id = int(el.find("Area").text)
        return obj

    @property
    def area(self):
        return self._vantage.areas.get(self.area_id)

@dataclass
class OmniSensor(VantageObject):
    level: Optional[float] = None

@dataclass
class Task(VantageObject):
    pass

@dataclass
class Variable(VantageObject):
    # TODO
    #   find("Tag") (Number/Text/etc)
    #   find("data/val") for numbers
    #   find("data/string") for text
    pass