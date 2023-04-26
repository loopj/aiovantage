import asyncio
import os

from aiovantage import Vantage

# Set your Vantage host ip, username, and password as environment variables
VANTAGE_HOST = os.getenv("VANTAGE_HOST", "vantage.local")
VANTAGE_USER = os.getenv("VANTAGE_USER")
VANTAGE_PASS = os.getenv("VANTAGE_PASS")


async def main() -> None:
    async with Vantage(VANTAGE_HOST, VANTAGE_USER, VANTAGE_PASS) as vantage:
        await vantage.areas.initialize()
        await vantage.loads.initialize()

        while True:
            on_loads = list(vantage.loads.on)
            print(f"{len(on_loads)} loads are ON")
            for load in on_loads:
                area = vantage.areas.get(load.area_id)
                print(f"- {load.name} ({area.name if area else 'Unknown Area'})")
            print()

            await asyncio.sleep(5)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
