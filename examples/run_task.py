import argparse
import asyncio
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
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

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


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
