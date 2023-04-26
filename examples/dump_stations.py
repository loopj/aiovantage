import asyncio
import os

from aiovantage import Vantage

# Set your Vantage host ip, username, and password as environment variables
VANTAGE_HOST = os.getenv("VANTAGE_HOST", "vantage.local")
VANTAGE_USER = os.getenv("VANTAGE_USER")
VANTAGE_PASS = os.getenv("VANTAGE_PASS")

# Some ANSI escape codes for pretty printing
RESET = "\033[0m"
YELLOW = "\033[33m"
CYAN = "\033[36m"


async def main() -> None:
    async with Vantage(VANTAGE_HOST, VANTAGE_USER, VANTAGE_PASS) as vantage:
        await vantage.initialize()

        for station in vantage.stations:
            print(f"{CYAN}{station.name}{RESET}")

            buttons = list(vantage.buttons.filter(parent_id=station.id))
            if buttons:
                print(f"    {YELLOW}Buttons{RESET}")
                for button in vantage.buttons.filter(parent_id=station.id):
                    print(f"    - {button.name}")
                print()

            dry_contacts = list(vantage.dry_contacts.filter(parent_id=station.id))
            if dry_contacts:
                print(f"    {YELLOW}Dry Contacts{RESET}")
                for dry_contact in dry_contacts:
                    print(f"    - {dry_contact.name}")
                print()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
