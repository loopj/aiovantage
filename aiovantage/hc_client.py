import asyncio
import logging
import shlex
import ssl

from collections import defaultdict

# TODO: Error handling
#   R:ERROR:4 "Invalid Parameter"
#   R:ERROR:5 "Wrong Number of Parameters"
#   R:ERROR:8 "Not Implemented"
#   R:ERROR:21 "Requires Login"
#   R:ERROR:23 "Login Failed"

# TODO: Automatically reconnect if connection is lost

STATUS_TYPES = ("LOAD", "LED", "BTN", "TASK", "TEMP", "THERMFAN", "THERMOP",
                "THERMDAY", "SLIDER", "TEXT", "VARIABLE", "BLIND", "PAGE",
                "LEDSTATE", "IMAGE", "WIND", "LIGHT", "CURRENT", "POWER")

class HCClient:
    """Communicate with a Vantage InFusion HC service.

    The HC service is a text-based service that allows interaction with devices
    controlled by a Vantage InFusion Controller.

    Among other things, this service allows you to change the state of devices
    (eg. turn on/off a light) as well as subscribe to status changes for devices.

    My guess is that HC stands for "Home Control".
    """

    def __init__(self, host, username=None, password=None, use_ssl=True, port=None):
        self._host = host
        self._username = username
        self._password = password
        self._use_ssl = use_ssl

        self._status_callbacks = defaultdict(list)
        self._tasks = []

        self._logger = logging.getLogger(__name__)

        if port is None:
            self._port = 3010 if use_ssl else 3001

        if use_ssl:
            self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)

    async def __aenter__(self):
        """Return Context manager."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb):
        """Exit context manager."""
        await self.close()

    async def initialize(self):
        """Connect to the HC service and authenticate if necessary."""

        # Open a connection to the controller
        self._reader, self._writer = await asyncio.open_connection(
            self._host, self._port, ssl=self._ssl_context
        )

        self._logger.info("Connected")

        # Login if we have a username and password
        if self._username is not None and self._password is not None:
            await self.send_sync(f"LOGIN {self._username} {self._password}")
            self._logger.info("Login successful")

        # Start a background task to monitor incoming messages
        self._tasks.append(asyncio.create_task(self.__event_reader()))

    async def close(self):
        for task in self._tasks:
            task.cancel()

        self._tasks.clear()

    async def send(self, command):
        self._writer.write((command + "\r\n").encode())
        await self._writer.drain()

    async def send_sync(self, command):
        await self.send(command)
        response = await self.readline()
        if response.startswith("R:ERROR"):
            _, error_message = shlex.split(response[2:])
            raise Exception(error_message)
        elif not response.startswith(f"R:{command.split()[0]}"):
            raise Exception("Received out of order response")

    async def readline(self):
        reply = await self._reader.readline()
        return reply.decode().rstrip()

    async def subscribe(self, callback, *status_types):
        for status_type in status_types:
            if status_type not in STATUS_TYPES:
                raise Exception(f"Invalid status type '{status_type}'")

            await self.send(f"STATUS {status_type}")
            self._status_callbacks[status_type].append(callback)

    async def __event_reader(self):
        while True:
            message = await self.readline()
            if message.startswith("S:"):
                # Parse status messages (eg. "S:LOAD 118 100.00")
                status_type, vid, *args = shlex.split(message[2:])
                for callback in self._status_callbacks[status_type]:
                    callback(status_type, int(vid), args)
            elif message.startswith("R:"):
                pass