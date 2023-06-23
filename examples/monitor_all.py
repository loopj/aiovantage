"""Fetch all objects from the Vantage controller, and print out any state changes."""

import argparse
import asyncio
import contextlib
import logging
from typing import Any, Dict

from aiovantage import Vantage, VantageEvent
from aiovantage.config_client.objects import SystemObject


def callback(event: VantageEvent, obj: SystemObject, data: Dict[str, Any]) -> None:
    """Print out any state changes."""
    object_type = type(obj).__name__

    if event == VantageEvent.OBJECT_ADDED:
        print(f"[{object_type} added] '{obj.name}' ({obj.id})")
    elif event == VantageEvent.OBJECT_UPDATED:
        print(f"[{object_type} updated] '{obj.name}' ({obj.id})")
        for attr in data.get("attrs_changed", []):
            print(f"    {attr} = {getattr(obj, attr)}")


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="aiovantage example")
    parser.add_argument("host", help="hostname of Vantage controller")
    parser.add_argument("--username", help="username for Vantage controller")
    parser.add_argument("--password", help="password for Vantage controller")
    parser.add_argument(
        "--debug", help="enable debug level logging", action="store_true"
    )
    parser.add_argument("--log", help="write debug log to file")
    return parser.parse_args()


def configure_logging(log_args: argparse.Namespace) -> None:
    """Configure debug logging."""
    logging.basicConfig(
        level=logging.DEBUG if log_args.debug else logging.INFO,
        format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )
    if log_args.log:
        logging.getLogger().addHandler(logging.FileHandler(filename=args.log, mode='w'))


# Parse command line args and configure logging
args = parse_arguments()
configure_logging(args)


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Connect to the Vantage controller
    async with Vantage(args.host, args.username, args.password) as vantage:
        # Subscribe to updates for all objects
        vantage.subscribe(callback)

        # Fetch all known objects from the controller
        await vantage.initialize()

        # Keep running for a while
        await asyncio.sleep(3600)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main(), debug=args.debug)
