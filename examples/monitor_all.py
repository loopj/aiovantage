import argparse
import asyncio
from typing import Any, Dict

from aiovantage import Vantage
from aiovantage.config_client.system_objects import SystemObject
from aiovantage.vantage.controllers.base import ControllerEventType

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


def callback(
    event: ControllerEventType, obj: SystemObject, data: Dict[str, Any]
) -> None:
    object_type = type(obj).__name__

    if event == ControllerEventType.OBJECT_ADDED:
        print(f"[{object_type} added] '{obj.name}' ({obj.id})")
    elif event == ControllerEventType.OBJECT_UPDATED:
        print(f"[{object_type} updated] '{obj.name}' ({obj.id})")
        for attr in data.get("attrs_changed", []):
            print(f"    {attr} = {getattr(obj, attr)}")


async def main() -> None:
    async with Vantage(args.host, args.username, args.password) as vantage:
        # Subscribe to updates for all objects
        vantage.subscribe(callback)

        # Fetch all known objects from the controller
        await vantage.initialize()

        # Keep running for a while
        await asyncio.sleep(3600)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
