# python3 -m tests.mock_hc_server

import asyncio
import random
import socket
from typing import Set

from .common import ObjectStore

VALID_STATUS_TYPES = ("LOAD", "LED", "BTN", "TASK", "TEMP", "VARIABLE")


class MockHCSession:
    def __init__(
        self, writer: asyncio.StreamWriter, id: int, objects: ObjectStore
    ) -> None:
        self.writer = writer
        self.id = id
        self.status_all = False
        self.status_types: Set[str] = set()
        self.status_ids: Set[int] = set()
        self._objects = objects

        print(f"Client {self.id} connected.")

    async def send_message(self, message: str) -> None:
        self.writer.write(message.encode() + b"\r\n")
        await self.writer.drain()

    async def handle_command(self, message: str) -> None:
        command, *args = message.split(" ")
        command = command.upper()

        if command == "STATUS":
            # STATUS {type}

            if len(args) != 1:
                await self.send_message('R:ERROR:5 "Wrong Number of Parameters"')
                return

            status_type = args[0].upper()
            if status_type == "ALL":
                self.status_all = True
                await self.send_message(f"R:STATUS {args[0]}")
            elif status_type == "NONE":
                self.status_all = False
                self.status_types.clear()
                await self.send_message(f"R:STATUS {args[0]}")
            elif status_type in VALID_STATUS_TYPES:
                self.status_types.add(status_type)
                await self.send_message(f"R:STATUS {args[0]}")
                print(f"Client {self.id} subscribed to status type {status_type}")
            else:
                await self.send_message('R:ERROR:4 "Invalid Parameter"')

        elif command == "ADDSTATUS":
            # ADDSTATUS {id1} {id2} ...

            ids_str = args[:16]
            self.status_ids.update(map(int, ids_str))
            await self.send_message(f"R:ADDSTATUS {' '.join(ids_str)}")
            print(f"Client {self.id} subscribed to object ids {ids_str}")

        elif command == "DELSTATUS":
            # DELSTATUS {id1} {id2} ...

            ids_str = args[:16]
            self.status_ids.difference_update(map(int, ids_str))
            await self.send_message(f"R:DELSTATUS {' '.join(ids_str)}")
            print(f"Client {self.id} unsubscribed from object ids {ids_str}")

        elif command == "LISTSTATUS":
            # LISTSTATUS

            for id in self.status_ids:
                await self.send_message(f"SL: {id}")
            await self.send_message("R:LISTSTATUS")

        elif command == "GETLOAD":
            # GETLOAD {id}

            if len(args) != 1:
                await self.send_message('R:ERROR:5 "Wrong Number of Parameters"')
                return

            id = int(args[0])
            if not self._objects.exists(id):
                await self.send_message('R:ERROR:7 "Invalid VID"')
                return

            await self.send_message(f"R:GETLOAD {id} {self._objects.loads[id].level}")

        elif command == "LOAD":
            # LOAD {id} {level}

            if len(args) != 2:
                await self.send_message('R:ERROR:5 "Wrong Number of Parameters"')
                return

            id = int(args[0])
            if not self._objects.exists(id):
                await self.send_message('R:ERROR:7 "Invalid VID"')
                return

            level = max(min(int(args[1]), 100), 0)
            self._objects.loads[id].level = level
            await self.send_message(f"R:LOAD {id} {level}")
            await self.send_message(f"S:LOAD {id} {level}")

        else:
            print(f"Client {self.id} sent unknown command {command}")

            response = command.upper()
            if args:
                response += " " + " ".join(args)
            await self.send_message(f"R:{response}")

    async def close(self) -> None:
        print(f"Client {self.id} disconnected.")


class MockHCServer:
    def __init__(self) -> None:
        self._sessions: Set[MockHCSession] = set()
        self._objects = ObjectStore()

    async def handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        session = MockHCSession(writer, len(self._sessions) + 1, self._objects)
        self._sessions.add(session)

        try:
            while True:
                data = await reader.readline()
                if not data:
                    break

                command = data.decode().rstrip()
                await session.handle_command(command)
        finally:
            self._sessions.discard(session)
            await session.close()

    async def start(self) -> None:
        # Create the server
        server = await asyncio.start_server(
            self.handle_client, "localhost", 3001, family=socket.AF_INET
        )

        # Get the server address
        addr = server.sockets[0].getsockname()
        print(f"Mock Host Command service started at {addr[0]}:{addr[1]}")

        # Run the server indefinitely
        async with server:
            await server.serve_forever()

    async def load_updated(self, id: int, level: int) -> None:
        for session in self._sessions:
            if session.status_all or (
                id in self._objects.loads and "LOAD" in session.status_types
            ):
                self._objects.loads[id].level = level
                await session.send_message(f"S:LOAD {id} {level}")


async def random_status_updates(server: MockHCServer) -> None:
    while True:
        id = random.choice(list(server._objects.loads.keys()))
        await server.load_updated(id, random.randint(0, 100))
        await asyncio.sleep(random.uniform(0, 10))


async def main() -> None:
    server = MockHCServer()
    asyncio.create_task(random_status_updates(server))
    await server.start()


asyncio.run(main())
