import argparse
import asyncio
import logging
from typing import Any, Dict

from aiovantage import Vantage, VantageEvent
from aiovantage.config_client.objects import Load

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--no-ssl", help="use non-ssl connection", action="store_true")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


def callback(event: VantageEvent, obj: Load, data: Dict[str, Any]) -> None:
    if event == VantageEvent.OBJECT_ADDED:
        print(f"[Load added] '{obj.name}' ({obj.id})")

    elif event == VantageEvent.OBJECT_UPDATED:
        print(f"[Load updated] '{obj.name}' ({obj.id})")
        for attr in data.get("attrs_changed", []):
            print(f"    {attr} = {getattr(obj, attr)}")


async def main() -> None:
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    async with Vantage(
        args.host, args.username, args.password, use_ssl=not args.no_ssl
    ) as vantage:
        # Subscribe to updates for all loads
        vantage.loads.subscribe(callback)

        # Fetch all known loads from the controller
        await vantage.loads.initialize()

        # Keep running for a while
        await asyncio.sleep(3600)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
