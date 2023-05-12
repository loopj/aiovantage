import asyncio
import socket
from typing import Set


class Client:
    def __init__(self, writer: asyncio.StreamWriter, id: int) -> None:
        self.writer = writer
        self.id = id

        print(f"Client {self.id} connected.")

    async def close(self) -> None:
        print(f"Client {self.id} disconnected.")


clients: Set[Client] = set()


async def handle_client(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    client = Client(writer, len(clients) + 1)
    clients.add(client)

    results_finished = False

    try:
        while True:
            data = await reader.read(1000)
            if not data:
                break

            message = data.decode()
            print(message)
            if "<IConfiguration><OpenFilter>" in message:
                writer.write("<IConfiguration><OpenFilter><return>123</return></OpenFilter></IConfiguration>\n".encode())
            elif "<IConfiguration><GetFilterResults>" in message:
                if results_finished:
                    writer.write('<IConfiguration><GetFilterResults><return></return></GetFilterResults></IConfiguration>\n'.encode())
                else:
                    writer.write('<IConfiguration><GetFilterResults><return><Object VID="1"><Load VID="1" Master="1" MTime="2023-05-05T05:03:16.526"><Name>Light</Name><LoadType>Incandescent</LoadType><PowerProfile>1</PowerProfile><DName/><Model/><Note/><Area>1</Area><Location/></Load></Object></return></GetFilterResults></IConfiguration>\n'.encode())
                    results_finished = True
            elif "<IConfiguration><CloseFilter>" in message:
                writer.write('<IConfiguration><CloseFilter><return>true</return></CloseFilter></IConfiguration>\n'.encode())
            await writer.drain()

    finally:
        clients.discard(client)
        await client.close()


async def main() -> None:
    # Create the server
    server = await asyncio.start_server(
        handle_client, "localhost", 2001, family=socket.AF_INET
    )
    addr = server.sockets[0].getsockname()
    print(f"Mock ACI service started at {addr[0]}:{addr[1]}")

    # Start the server
    async with server:
        await server.serve_forever()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Server stopped.")
