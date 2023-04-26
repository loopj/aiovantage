import asyncio
import os

from aiovantage import Vantage

# Set your Vantage host ip, username, and password as environment variables
VANTAGE_HOST = os.getenv("VANTAGE_HOST", "vantage.local")
VANTAGE_USER = os.getenv("VANTAGE_USER")
VANTAGE_PASS = os.getenv("VANTAGE_PASS")


async def main() -> None:
    async with Vantage(VANTAGE_HOST, VANTAGE_USER, VANTAGE_PASS) as vantage:
        await vantage.loads.initialize()
        for load in vantage.loads:
            print(f"{load.name}")


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
