import asyncio
import logging
import shlex
from inspect import iscoroutinefunction
from itertools import islice
from ssl import PROTOCOL_TLS, SSLContext
from types import TracebackType
from typing import Callable, Iterable, List, Optional, Tuple, Type, Union, overload

from .errors import CommandExecutionError, LoginFailedError, LoginRequiredError


# Type for callbacks that are called when a status update is received
StatusCallback = Callable[[str, int, List[str]], None]

# Type for a status subscription (a callback with an optional type filter)
StatusSubscription = Tuple[StatusCallback, Optional[Iterable[str]]]


class HCClient:
    """Communicate with a Vantage InFusion Host Command service.

    The Host Command service is a TCP text-based service that allows interaction with
    devices controlled by a Vantage InFusion Controller.

    Among other things, this service allows you to change the state of devices
    (eg. turn on/off a light) as well as subscribe to status changes for devices.

    The service is exposed by the controller on port 3010, and uses SSL by default.
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
        self._subscriptions: List[StatusSubscription] = []
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
        await self.connect()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self.close()

    async def connect(self) -> None:
        """Connect to the Host Command service, authenticating if necessary."""

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
        if self._username and self._password:
            await self.login(self._username, self._password)

    async def close(self) -> None:
        """Close the connection to the service and cancel any running tasks."""

        # Cancel any running tasks
        for task in self._tasks:
            task.cancel()
        self._tasks = []

        # Check if the connection is already closed
        if self._writer is None or self._writer.is_closing():
            return

        # Close the connection
        self._writer.close()
        await self._writer.wait_closed()

        self._logger.debug("Connection closed")

    async def raw_request(self, request: str) -> List[str]:
        """
        Send a raw string request to the Host Command service, returning all lines of
        the response, until the "R:" line is received.

        Args:
            request: The request string to send.

        Returns:
            A list of response lines.
        """

        # TODO: Connect if not connected, or at least raise an error
        # TODO: Add a timeout

        # Send the request
        self._logger.debug(f"Sending request: {request}")
        self._writer.write(f"{request}\n".encode())  # type: ignore[union-attr]
        await self._writer.drain()  # type: ignore[union-attr]

        # Grab every line of the response, until we get a "return" line
        response = []
        while True:
            line = await self._response_queue.get()
            self._response_queue.task_done()
            response.append(line)
            if line.startswith("R:"):
                break

        return response

    async def command(self, command: str, *params: Union[int, float, str]) -> List[str]:
        """
        Send a command with parameters to the Host Command service, and return the
        arguments of the "R:" line of the response.

        Handles encoding the parameters correctly, and raises an exception if the
        response line is R:ERROR.

        Args:
            command: The command to send, should be a single word string.
            params: The parameters to send with the command, int, float, or str.

        Returns:
            A list of response arguments.
        """

        if not all(isinstance(param, (int, float, str)) for param in params):
            raise TypeError("Command parameters must be int, float, or str")

        # Build the request string, encoding the parameters if necessary
        if params:
            request = f"{command} {' '.join([str(p) for p in params])}"
        else:
            request = command

        # Send the request
        response_lines = await self.raw_request(request)

        # Get the "R:" return line and split it into parts
        response = response_lines[-1]
        reply, *args = shlex.split(response)

        # Check for errors
        if reply.startswith("R:ERROR"):
            _, _, error_code_str = reply.split(":")
            error_code = int(error_code_str)
            error_message = args[0]
            if error_code == 21:
                raise LoginRequiredError(error_message)
            elif error_code == 23:
                raise LoginFailedError(error_message)
            else:
                raise CommandExecutionError(
                    f"{error_message} (Error code {error_code})"
                )

        # Check for out of order responses
        if not reply == f"R:{command.upper()}":
            raise Exception(
                f"Received out of order response."
                f"\tExpected: {command}"
                f"\tReceived: {response}"
            )

        return args

    async def invoke(
        self, id: int, method: str, *params: Union[int, float, str]
    ) -> List[str]:
        """Send an INVOKE command to invoke a method on an Vantage object.

        Args:
            id: The id of the object to invoke the method on.
            method: The name of the method to invoke.
            params: The parameters to pass to the method.

        Returns:
            A list of response arguments.
        """

        return await self.command("INVOKE", id, method, *params)

    async def login(self, username: str, password: str) -> None:
        """Send a LOGIN command to authenticate with the Host Command service.

        Args:
            username: The username to authenticate with.
            password: The password to authenticate with.
        """

        await self.command("LOGIN", username, password)

        self._logger.info("Logged in")

    async def addstatus(self, ids: Iterable[int]) -> None:
        """Send an ADDSTATUS command to subscribe to status events for the given ids.

        Args:
            ids: The ids to subscribe to status events for.
        """

        # ADDSTATUS accepts up to 16 ids at a time, so chunk the requests.
        id_iter = iter(ids)
        while id_chunk := tuple(islice(id_iter, 16)):
            await self.command("ADDSTATUS", *id_chunk)

    async def delstatus(self, ids: Iterable[int]) -> None:
        """Send a DELSTATUS command to unsubscribe from status events for the given ids.

        Args:
            ids: The ids to unsubscribe from status events for.
        """

        # DELSTATUS accepts up to 16 ids at a time, so chunk the requests.
        id_iter = iter(ids)
        while id_chunk := tuple(islice(id_iter, 16)):
            await self.command("DELSTATUS", *id_chunk)

    @overload
    async def subscribe(self, callback: StatusCallback) -> Callable[[], None]:
        """
        Subscribe to all status events.

        Args:
            callback: The callback to call when a status event is received.

        Returns:
            A function to unsubscribe from status events.
        """
        ...

    @overload
    async def subscribe(
        self, callback: StatusCallback, *, object_ids: Iterable[int]
    ) -> Callable[[], None]:
        """
        Subscribe to status events for the given object ids.

        Args:
            callback: The callback to call when a status event is received.
            object_ids: The ids to subscribe to status events for.

        Returns:
            A function to unsubscribe from status events.
        """
        ...

    @overload
    async def subscribe(
        self, callback: StatusCallback, *, status_types: Iterable[str]
    ) -> Callable[[], None]:
        """
        Subscribe to status events for the given status types.

        Args:
            callback: The callback to call when a status event is received.
            status_types: The status types to subscribe to status events for.

        Returns:
            A function to unsubscribe from status events.
        """
        ...

    async def subscribe(
        self,
        callback: StatusCallback,
        *,
        object_ids: Optional[Iterable[int]] = None,
        status_types: Optional[Iterable[str]] = None,
    ) -> Callable[[], None]:
        if object_ids is not None and status_types is not None:
            raise ValueError("Cannot specify both object_ids and status_types.")

        subscription: StatusSubscription
        if object_ids is not None:
            # Subscribe to status events for these object ids
            subscription = (callback, ("STATUS"))
            await self.addstatus(object_ids)
        elif status_types is not None:
            # Subscribe to status events of these types
            subscription = (callback, status_types)
            for status_type in status_types:
                await self.command("STATUS", status_type)
        else:
            # Subscribe to all status events
            subscription = (callback, None)
            await self.command("STATUS", "ALL")

        self._subscriptions.append(subscription)

        # Return a function to unsubscribe
        def unsubscribe() -> None:
            if object_ids is not None:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(self.delstatus(object_ids))
            elif status_types is not None:
                # TODO: Unsubscribe from specific status types if we were the last
                # subscriber for that type
                pass
            else:
                # TODO: ??? (STATUS NONE?)
                pass

            self._subscriptions.remove(subscription)

        return unsubscribe

    async def _handle_messages(self) -> None:
        # Fetch new messages from the reader and enqueue them for processing

        # TODO: Handle lost connection, auto-reconnect
        # - ConnectionResetError from the reader
        # - what else?

        while True:
            data = await self._reader.readline()  # type: ignore[union-attr]
            message = data.decode().rstrip()

            self._logger.debug(f"Received message: {message}")

            if message.startswith("S:"):
                self._status_queue.put_nowait(message[2:])
            else:
                self._response_queue.put_nowait(message)

    async def _status_processor(self) -> None:
        # Process status messages from the status queue and dispatch to subscribers

        while True:
            message = await self._status_queue.get()
            self._status_queue.task_done()

            status_type, vid_str, *args = shlex.split(message)
            vid = int(vid_str)

            for callback, filters in self._subscriptions:
                if filters is None or status_type in filters:
                    if iscoroutinefunction(callback):
                        asyncio.create_task(callback(status_type, vid, args))
                    else:
                        callback(status_type, vid, args)
