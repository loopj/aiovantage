import asyncio
import logging
from typing import List

from aiovantage import Vantage
from aiovantage.aci_client.system_objects import SystemObject

logging.basicConfig(level=logging.INFO)


# This callback will be called whenever an object is updated
def event_callback(obj: SystemObject, attrs_changed: List[str]) -> None:
    print(f"[{type(obj).__name__}] '{obj.name}' ({obj.id}) updated:")
    for attr in attrs_changed:
        print(f"    {attr} = {getattr(obj, attr)}")


async def main() -> None:
    async with Vantage("10.2.0.103", "administrator", "ZZuUw76CnL") as vantage:
        # Fetch objects from the controller
        await vantage.initialize()

        # Subscribe to status updates for all objects
        vantage.subscribe(event_callback)

        # Keep running for a while
        await asyncio.sleep(3600)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
