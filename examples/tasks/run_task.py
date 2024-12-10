"""Run a task by id."""

import argparse
import asyncio
import contextlib
import logging

from aiovantage import Vantage

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("id", help="task id to run")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Connect to the Vantage controller
    async with Vantage(args.host, args.username, args.password) as vantage:
        # Look up the task
        try:
            task_id = int(args.id)
        except ValueError:
            print("Invalid task id")
            return

        task = await vantage.tasks.aget(task_id)
        if task is None:
            print("Task not found")
            return

        # Run the task
        print(f"{task.name} (id = {task.id})")
        await task.start()


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
