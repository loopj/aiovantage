import argparse
import asyncio

from aiovantage import Vantage

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()

# Some ANSI escape codes for pretty printing
RESET = "\033[0m"
YELLOW = "\033[33m"
CYAN = "\033[36m"


async def main() -> None:
    async with Vantage(args.host, args.username, args.password) as vantage:
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
