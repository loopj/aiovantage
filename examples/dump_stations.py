import asyncio
import logging

from aiovantage import Vantage

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    async with Vantage("10.2.0.103", "administrator", "ZZuUw76CnL") as vantage:
        await vantage.initialize()

        for station in vantage.stations:
            print(f"{station.name}")

            print("    Buttons:")
            for button in vantage.buttons.filter(parent=station.id):
                print(f"        {button.name}")

            print("    Dry Contacts:")
            for dry_contact in vantage.dry_contacts.filter(parent=station.id):
                print(f"        {dry_contact.name}")


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
