import asyncio
import logging
from typing import List

from aiovantage import Vantage
from aiovantage.aci_client.system_objects import SystemObject

logging.basicConfig(level=logging.INFO)


# This callback will be called whenever a load is updated
def event_callback(obj: SystemObject, attrs_changed: List[str]) -> None:
    print(f"[{type(obj).__name__}] '{obj.name}' ({obj.id}) updated:")
    for attr in attrs_changed:
        print(f"    {attr} = {getattr(obj, attr)}")


async def main() -> None:
    async with Vantage("10.2.0.103", "administrator", "ZZuUw76CnL") as vantage:
        # Fetch all known loads from the controller
        await vantage.loads.initialize()
        await vantage.rgb_loads.initialize()

        # Subscribe to status updates for all loads
        vantage.loads.subscribe(event_callback)
        vantage.rgb_loads.subscribe(event_callback)

        # Keep running for a while
        await asyncio.sleep(3600)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
