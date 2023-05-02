import asyncio
import random
import socket
import struct
from typing import Set

VALID_STATUS_TYPES = ("LOAD", "LED", "BTN", "TASK", "TEMP", "VARIABLE")
LOADS = {
    1: {"level": 0},
    2: {"level": 0},
}
KNOWN_OBJECTS = LOADS.keys()


class Client:
    def __init__(self, writer: asyncio.StreamWriter, id: int) -> None:
        self.writer = writer
        self.id = id
        self.status_all = False
        self.status_types: Set[str] = set()
        self.status_ids: Set[int] = set()

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
        elif command == "GETLOAD":
            # GETLOAD {id}

            if len(args) != 1:
                await self.send_message('R:ERROR:5 "Wrong Number of Parameters"')
                return

            id = int(args[0])
            if id not in KNOWN_OBJECTS:
                await self.send_message('R:ERROR:7 "Invalid VID"')
                return

            await self.send_message(f"R:GETLOAD {id} {LOADS[id]['level']}")
        elif command == "LOAD":
            # LOAD {id} {level}

            if len(args) != 2:
                await self.send_message('R:ERROR:5 "Wrong Number of Parameters"')
                return

            id = int(args[0])
            if id not in KNOWN_OBJECTS:
                await self.send_message('R:ERROR:7 "Invalid VID"')
                return

            level = max(min(int(args[1]), 100), 0)
            LOADS[id]["level"] = level
            await self.send_message(f"R:LOAD {id} {level}")
            await self.send_message(f"S:LOAD {id} {level}")
        else:
            response = command.upper()
            if args:
                response += " " + " ".join(args)
            await self.send_message(f"R:{response}")

    async def close(self) -> None:
        print(f"Client {self.id} disconnected.")


clients: Set[Client] = set()


async def random_status_updates() -> None:
    while True:
        for client in clients:
            id = random.choice(list(KNOWN_OBJECTS))

            if client.status_all or id in LOADS:
                load = LOADS[id]
                load["level"] = random.randint(0, 100)
                await client.send_message(f"S:LOAD {id} {load['level']}")

        await asyncio.sleep(random.random() * 20)


async def close_socket() -> None:
    await asyncio.sleep(10)
    for client in clients:
        print(f"Closing client {client.id}")
        client.writer.close()


async def handle_client(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    client = Client(writer, len(clients) + 1)
    clients.add(client)
    print(f"New client connected. {len(clients)} clients connected.")

    try:
        while True:
            data = await reader.read(100)
            if not data:
                break

            command = data.decode().rstrip()
            await client.handle_command(command)
    finally:
        clients.discard(client)
        await client.close()


async def main() -> None:
    # Start the server
    server = await asyncio.start_server(handle_client, "localhost", 3001)
    server_sock = server.sockets[0]
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))

    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    # Start the random status updates
    asyncio.create_task(random_status_updates())
    # asyncio.create_task(close_socket())

    async with server:
        await server.serve_forever()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Server stopped.")
