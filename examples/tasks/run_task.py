"""Run a task by id."""

import asyncio
import contextlib

from aiovantage import Vantage

from debug_logging import configure_logging, parse_arguments

# Grab connection info from command line arguments
args = parse_arguments()


async def main() -> None:
    """Run code example."""
    configure_logging(args.debug)

    # Connect to the Vantage controller and print out the name and value of each GMem
    async with Vantage(args.host, args.username, args.password) as vantage:
        try:
            task_id = int(args.id)
        except ValueError:
            print("Invalid task id")
            return

        task = await vantage.tasks.aget(task_id)
        if task is None:
            print("Task not found")
            return

        print(f"{task.name} (id = {task.id})")
        await vantage.tasks.start(task.id)


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main(), debug=args.debug)
