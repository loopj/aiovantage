import asyncio
import logging
import shlex
import ssl
from enum import Enum
from types import NoneType, TracebackType
from typing import Callable, List, Optional, Tuple, Type, Union


class LoginRequiredError(Exception):
    pass


class LoginFailedError(Exception):
    pass


class StatusType(Enum):
    LOAD = "LOAD"
    LED = "LED"
    BTN = "BTN"
    TASK = "TASK"
    TEMP = "TEMP"
    THERMFAN = "THERMFAN"
    THERMOP = "THERMOP"
    THERMDAY = "THERMDAY"
    SLIDER = "SLIDER"
    TEXT = "TEXT"
    VARIABLE = "VARIABLE"
    BLIND = "BLIND"
    PAGE = "PAGE"
    LEDSTATE = "LEDSTATE"
    IMAGE = "IMAGE"
    WIND = "WIND"
    LIGHT = "LIGHT"
    CURRENT = "CURRENT"
    POWER = "POWER"


EventCallBackType = Callable[[StatusType, int, List[str]], None]
EventSubscriptionType = Tuple[
    EventCallBackType,
    "Optional[Tuple[StatusType, ...]]",
]


class HCClient:
    """Communicate with a Vantage InFusion HC service.

    The HC service is a text-based service that allows interaction with devices
    controlled by a Vantage InFusion Controller.

    Among other things, this service allows you to change the state of devices
    (eg. turn on/off a light) as well as subscribe to status changes for devices.

    My guess is that HC stands for "Home Control".
    """

    def __init__(
        self,
        host: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_ssl: bool = True,
        port: Optional[int] = None,
    ) -> None:
        self._host = host
        self._username = username
        self._password = password
        self._use_ssl = use_ssl
        self._tasks: List[asyncio.Task] = []
        self._subscribers: List[EventSubscriptionType] = []
        self._response_queue: asyncio.Queue[str] = asyncio.Queue()
        self._status_queue: asyncio.Queue[str] = asyncio.Queue()
        self._logger = logging.getLogger(__name__)

        if port is None:
            self._port = 3010 if use_ssl else 3001

        if use_ssl:
            self._ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)

    async def __aenter__(self) -> "HCClient":
        """Return Context manager."""
        await self.initialize()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Close context manager."""
        await self.close()

    async def initialize(self) -> None:
        """Connect to the HC service and authenticate if necessary."""

        # Open a connection to the controller
        self._reader, self._writer = await asyncio.open_connection(
            self._host, self._port, ssl=self._ssl_context
        )
        self._logger.info("Connected")

        # Start a task to handle incoming messages
        self._tasks.append(asyncio.create_task(self._handle_messages()))
        self._tasks.append(asyncio.create_task(self._status_processor()))
        self._logger.info("Message processing started")

        # Login if we have a username and password
        if self._username is not None and self._password is not None:
            await self.send_command("LOGIN", self._username, self._password)
            self._logger.info("Login successful")

    async def _handle_messages(self) -> None:
        while True:
            data = await self._reader.readline()
            message = data.decode().strip()
            if message.startswith("R:"):
                self._response_queue.put_nowait(message[2:])
            elif message.startswith("S:"):
                self._status_queue.put_nowait(message[2:])
            else:
                self._logger.warning(f"Received unknown message: {message}")

    async def _status_processor(self) -> None:
        while True:
            message = await self._status_queue.get()
            self._status_queue.task_done()

            type_str, vid_str, *args = shlex.split(message)
            type = StatusType(type_str)
            vid = int(vid_str)

            self.emit(type, vid, args)

    async def close(self) -> None:
        """Close the connection to the service and cancel any running tasks."""
        for task in self._tasks:
            task.cancel()
        self._tasks = []

        if self._writer is not None:
            self._writer.close()
            await self._writer.wait_closed()

    async def send_command(self, command: str, *params: str) -> str:
        # Join the command and parameters into a single string, escaping any
        # parameters that contain spaces with quotes
        params_str = " ".join(f'"{s}"' if " " in s else s for s in params)
        message = f"{command} {params_str}\n"

        # Send the command
        self._writer.write(message.encode())
        await self._writer.drain()

        # Wait for a response
        response = await self._response_queue.get()
        self._response_queue.task_done()

        # Check for errors
        if response.startswith("ERROR"):
            error_code, error_message = shlex.split(response)
            error_code = error_code.split(":")[1]
            if error_code == "4":
                raise TypeError(error_message)
            elif error_code == "5":
                raise TypeError(error_message)
            elif error_code == "8":
                raise NotImplementedError(error_message)
            elif error_code == "21":
                raise LoginRequiredError(error_message)
            elif error_code == "23":
                raise LoginFailedError(error_message)
            else:
                raise Exception(f"Unknown error code: {error_code}")
        elif not response.startswith(command):
            raise Exception(f"Received out of order response: {response}")

        return response

    async def subscribe(
        self,
        callback: EventCallBackType,
        status_filter: Union[StatusType, Tuple[StatusType, ...], None] = None,
    ) -> Callable:
        """Subscribe to status events."""

        # Support passing a single status type instead of a tuple
        if status_filter is not None and isinstance(status_filter, StatusType):
            status_filter = (status_filter,)

        # Tell the Vantage controller we are interested in status events
        # We try to only subscribe to what we know we care about
        if status_filter is None:
            await self.send_command("STATUS", "ALL")
        else:
            for status_type in status_filter:
                await self.send_command("STATUS", status_type.value)

        # Add the callback to the list of subscribers
        subscription = (callback, status_filter)
        self._subscribers.append(subscription)

        # Return a function that can be used to unsubscribe
        def unsubscribe() -> None:
            self._subscribers.remove(subscription)
        return unsubscribe

    def emit(self, type: StatusType, vid: int, args: List[str]) -> None:
        """Fire a status update event to all matching subscribers."""
        for callback, status_filter in self._subscribers:
            if status_filter is None or type in status_filter:
                callback(type, vid, args)
