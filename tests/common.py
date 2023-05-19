import json
import pathlib
from typing import Any, Dict

from xsdata.models.datatype import XmlDateTime

from aiovantage.config_client.objects import Area, Load, Keypad, Button, DryContact


def load_fixture(name: str) -> Any:
    path = pathlib.Path(__file__).parent / "fixtures" / name
    content = path.read_text()
    return json.loads(content)


class ObjectStore:
    def __init__(self) -> None:
        self.areas: Dict[int, Area] = {}
        self.loads: Dict[int, Load] = {}
        self.stations: Dict[int, Keypad] = {}
        self.buttons: Dict[int, Button] = {}
        self.dry_contacts: Dict[int, DryContact] = {}

        data = load_fixture("objects.json")

        for area_json in data["Area"]:
            area = Area(
                id=area_json["id"],
                master_id=1,
                mtime=XmlDateTime.from_string("2023-05-05T05:03:16.526"),
                name=area_json["name"],
                model="",
                note="",
                display_name="",
                area_id=area_json["area_id"],
                location="",
            )

            self.areas[area_json["id"]] = area

        for load_json in data["Load"]:
            load = Load(
                id=load_json["id"],
                master_id=1,
                mtime=XmlDateTime.from_string("2023-05-05T05:03:16.526"),
                name=load_json["name"],
                model="",
                note="",
                display_name="",
                area_id=load_json["area_id"],
                location="",
                load_type="Incandescent",
                power_profile_id=1,
            )

            load.level = 0

            self.loads[load_json["id"]] = load

        for station_json in data["Keypad"]:
            station = Keypad(
                id=station_json["id"],
                master_id=1,
                mtime=XmlDateTime.from_string("2023-05-05T05:03:16.526"),
                name=station_json["name"],
                model="",
                note="",
                display_name="",
                area_id=station_json["area_id"],
                location="",
                serial_number="123456",
                bus_id=1,
            )

            self.stations[station_json["id"]] = station

        for button_json in data["Button"]:
            button = Button(
                id=button_json["id"],
                master_id=1,
                mtime=XmlDateTime.from_string("2023-05-05T05:03:16.526"),
                name=button_json["name"],
                model="",
                note="",
                display_name="",
                parent_id=button_json["parent_id"],
                text1=button_json["text"],
                text2="",
            )

            self.buttons[button_json["id"]] = button

        for dry_contact_json in data["DryContact"]:
            dry_contact = DryContact(
                id=dry_contact_json["id"],
                master_id=1,
                mtime=XmlDateTime.from_string("2023-05-05T05:03:16.526"),
                name=dry_contact_json["name"],
                model="",
                note="",
                display_name="",
                area_id=dry_contact_json["area_id"],
                location="",
                parent_id=dry_contact_json["parent_id"],
            )

            self.dry_contacts[dry_contact_json["id"]] = dry_contact

    def exists(self, id: int) -> bool:
        return id in self.loads or id in self.areas
