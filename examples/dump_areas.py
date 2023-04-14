import asyncio
import logging

from aiovantage import Vantage
from aiovantage.aci_client.system_objects.area import Area

logging.basicConfig(level=logging.INFO)


def print_indented(text: str, indent_level: int) -> None:
    indent = indent_level * "    "
    print(indent + text)


def print_area(vantage: Vantage, area: Area, level: int = 0) -> None:
    print_indented(f"{area.name}", level)

    for child_area in vantage.areas.filter(area=area.id):
        print_area(vantage, child_area, level=level + 1)

    print_indented("Stations:", level + 1)
    for station in vantage.stations.filter(area=area.id):
        print_indented(f"{station.name}", level + 2)

    print_indented("Loads:", level + 1)
    for load in vantage.loads.filter(area=area.id):
        print_indented(f"{load.name}", level + 2)

    print_indented("Dry Contacts:", level + 1)
    for dry_contact in vantage.dry_contacts.filter(area=area.id):
        print_indented(f"{dry_contact.name}", level + 2)


async def main() -> None:
    async with Vantage("10.2.0.103", "administrator", "ZZuUw76CnL") as vantage:
        await vantage.initialize()

        root = vantage.areas.root()
        if root is not None:
            print_area(vantage, root)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
