import asyncio
import logging
import shlex
from enum import Enum
from inspect import iscoroutinefunction
from ssl import PROTOCOL_TLS, SSLContext
from types import TracebackType
from typing import Callable, Iterable, List, Optional, Sequence, Tuple, Type, Union

from .errors import LoginFailedError, LoginRequiredError


class StatusCategory(Enum):
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


CategoryEventCallback = Callable[[StatusCategory, int, Sequence[str]], None]
ObjectEventCallback = Callable[[int, str, Sequence[str]], None]
CategoryEventSubscription = Tuple[
    CategoryEventCallback,
    "Iterable[StatusCategory] | None",
]


def _encode_params(params: Sequence[Union[int, float, str]]) -> str:
    string_params = [str(p) for p in params]
    return " ".join(f'"{s}"' if " " in s else s for s in string_params)


class HCClient:
    """Communicate with a Vantage InFusion Host Command service.

    The Host Command service is a text-based service that allows interaction with
    devices controlled by a Vantage InFusion Controller.

    Among other things, this service allows you to change the state of devices
    (eg. turn on/off a light) as well as subscribe to status changes for devices.
    """

    def __init__(
        self,
        host: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        *,
        use_ssl: bool = True,
        port: Optional[int] = None,
        conn_timeout: float = 5,
    ) -> None:
        """
        Initialize the HCClient instance.

        Args:
            host: The hostname or IP address of the Host Command service.
            username: The username to use to authenticate.
            password: The password to use to authenticate.
            use_ssl: Whether to use SSL when connecting.
            port: The port to use when connecting.
            conn_timeout: The timeout to use when connecting.
        """

        self._host = host
        self._username = username
        self._password = password
        self._use_ssl = use_ssl
        self._tasks: List[asyncio.Task[None]] = []
        self._category_subscribers: List[CategoryEventSubscription] = []
        self._object_subscribers: List[ObjectEventCallback] = []
        self._response_queue: asyncio.Queue[str] = asyncio.Queue()
        self._status_queue: asyncio.Queue[str] = asyncio.Queue()
        self._logger = logging.getLogger(__name__)
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._conn_timeout = conn_timeout

        if port is None:
            self._port = 3010 if use_ssl else 3001
        else:
            self._port = port

        if use_ssl:
            self._ssl_context = SSLContext(PROTOCOL_TLS)

    async def __aenter__(self) -> "HCClient":
        """Return Context manager."""

        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Close context manager."""

        await self.close()

    async def connect(self) -> None:
        """Connect to the HC service, authenticate if necessary."""

        # Open a connection to the controller
        self._reader, self._writer = await asyncio.wait_for(
            asyncio.open_connection(
                self._host,
                self._port,
                ssl=self._ssl_context,
            ),
            timeout=self._conn_timeout,
        )

        # Start tasks to handle incoming messages
        self._tasks.append(asyncio.create_task(self._handle_messages()))
        self._tasks.append(asyncio.create_task(self._status_processor()))

        self._logger.info("Connected")

        # Login if we have a username and password
        await self._login()

    async def _handle_messages(self) -> None:
        while True:
            data = await self._reader.readline()  # type: ignore[union-attr]
            message = data.decode().strip()

            self._logger.debug(f"Received message: {message}")

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
            vid = int(vid_str)

            if type_str in StatusCategory.__members__:
                # Handle a category status message
                type = StatusCategory(type_str)

                for category_callback, category_filter in self._category_subscribers:
                    if category_filter is None or type in category_filter:
                        if iscoroutinefunction(category_callback):
                            asyncio.create_task(category_callback(type, vid, args))
                        else:
                            category_callback(type, vid, args)
            elif type_str == "STATUS":
                # Handle an object status message
                for obj_callback in self._object_subscribers:
                    if iscoroutinefunction(obj_callback):
                        asyncio.create_task(obj_callback(vid, args[0], args[1:]))
                    else:
                        obj_callback(vid, args[0], args[1:])
            else:
                self._logger.warning(f"Received unknown status message: {message}")

    async def close(self) -> None:
        """Close the connection to the service and cancel any running tasks."""

        for task in self._tasks:
            task.cancel()
        self._tasks = []

        if self._writer is None or self._writer.is_closing():
            return

        self._writer.close()
        await self._writer.wait_closed()

        self._logger.debug("Connection closed")

    async def send_raw_command(self, command: str, response_lines: int = 1) -> str:
        # Send the command
        self._writer.write(command.encode())  # type: ignore[union-attr]
        await self._writer.drain()  # type: ignore[union-attr]

        # Grab the first line of the response
        response = await self._response_queue.get()
        self._response_queue.task_done()

        # If we expected a multiple line response, pop the extra lines off the queue
        # We don't currently do anything with these lines
        if response_lines > 1:
            for _ in range(response_lines - 1):
                await self._response_queue.get()
                self._response_queue.task_done()

        return response

    async def send_command(
        self, command: str, *params: Union[int, float, str], response_lines: int = 1
    ) -> List[str]:
        """Send a command to the HC service, and wait for a response."""

        # Send the command and wait for a response
        message = f"{command} {_encode_params(params)}\n"
        response = await self.send_raw_command(message, response_lines)

        # Check for errors
        if response.startswith("ERROR"):
            error_code, error_message = shlex.split(response)
            error_code = error_code.split(":")[1]
            if error_code == "4":
                raise TypeError(error_message)
            elif error_code == "5":
                raise TypeError(error_message)
            elif error_code == "7":
                raise ValueError(error_message)
            elif error_code == "8":
                raise NotImplementedError(error_message)
            elif error_code == "21":
                raise LoginRequiredError(error_message)
            elif error_code == "23":
                raise LoginFailedError(error_message)
            else:
                raise Exception(f"Unknown error: {error_code} {error_message}")

        # Split the response into tokens
        rcommand, *rval = shlex.split(response)

        # Check for out of order responses
        if not rcommand.upper() == command.upper():
            raise Exception(
                f"Received out of order response."
                f"\tExpected: {command}"
                f"\tReceived: {response}"
            )

        return rval

    async def invoke(
        self, vid: int, method: str, *params: Union[int, float, str]
    ) -> List[str]:
        """Invoke a method on a Vantage object."""

        return await self.send_command("INVOKE", vid, method, *params)

    async def subscribe_category(
        self,
        callback: CategoryEventCallback,
        status_filter: Union[None, StatusCategory, Iterable[StatusCategory]] = None,
    ) -> Callable[[], None]:
        """
        Subscribe to category status events, optionally filtering by status category.
        """

        # Support passing a single status type instead of a tuple
        if status_filter is not None and isinstance(status_filter, StatusCategory):
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
        self._category_subscribers.append(subscription)

        # Return a function that can be used to unsubscribe
        def unsubscribe() -> None:
            self._category_subscribers.remove(subscription)

        return unsubscribe

    async def subscribe_objects(
        self,
        callback: ObjectEventCallback,
        vids: Iterable[int],
    ) -> Callable[[], None]:
        """Subscribe to status events for a specific object."""

        # TODO: ADDSTATUS accepts multiple vids (up to 16?)
        # TODO: only 64 vids can be tracked by ADDSTATUS per connection
        for vid in vids:
            await self.send_command("ADDSTATUS", f"{vid}")

        self._object_subscribers.append(callback)

        def unsubscribe() -> None:
            # TODO: Run this in a background task?
            # for vid in vids:
            #     await self.send_command("DELSTATUS", f"{vid}")

            self._object_subscribers.remove(callback)

        return unsubscribe

    async def _login(self) -> None:
        # Login to the HC service.

        if not self._username or not self._password:
            return

        await self.send_command("LOGIN", self._username, self._password)

        self._logger.info("Login successful")
