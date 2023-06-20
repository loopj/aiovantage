"""Client for the Vantage Application Communication Interface (ACI) service."""

import asyncio
import logging
from ssl import SSLContext
from types import TracebackType
from typing import Any, Optional, Type, Union

from typing_extensions import Self

from .connection import ConfigConnection
from .errors import LoginFailedError
from .methods import Call, Method, Return
from .methods.login import Login


class ConfigClient:
    """Client for the Vantage Application Communication Interface (ACI) service.

    This client handles connecting to the ACI service, authenticating, and the
    serialization/deserialization of XML requests and responses.
    """

    def __init__(
        self,
        host: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        *,
        ssl: Union[SSLContext, bool] = True,
        port: Optional[int] = None,
        conn_timeout: float = 5,
        read_timeout: float = 30,
    ):
        self._host = host
        self._username = username
        self._password = password
        self._ssl = ssl
        self._port = port
        self._conn_timeout = conn_timeout
        self._read_timeout = read_timeout
        self._connection: Optional[ConfigConnection] = None
        self._lock = asyncio.Lock()
        self._logger = logging.getLogger(__name__)

    async def __aenter__(self) -> Self:
        """Return context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit context manager."""
        self.close()
        if exc_val:
            raise exc_val

    def close(self) -> None:
        """Close the connection to the ACI service."""

        if self._connection is not None:
            self._connection.close()

    async def request(
        self, method_cls: Type[Method[Call, Return]], params: Any = None
    ) -> Return:
        """Marshall a request, send it to the ACI service, and yield a parsed object.

        Args:
            method_cls: The method class to use
            params: The parameters instance to pass to the method

        Returns:
            The parsed response object
        """

        conn = await self._get_connection()
        return await conn.request(method_cls, params)

    async def _get_connection(self) -> ConfigConnection:
        """Get a connection to the ACI service, authenticating if necessary."""

        async with self._lock:
            if not (self._connection is None or self._connection.closed):
                return self._connection

            conn = ConfigConnection(
                self._host,
                self._port,
                ssl=self._ssl,
                conn_timeout=self._conn_timeout,
                read_timeout=self._read_timeout,
            )
            await conn.open()

            # Log in if we have credentials
            if self._username is not None and self._password is not None:
                success = await conn.request(
                    Login, Login.Params(self._username, self._password)
                )

                if not success:
                    raise LoginFailedError("Login failed, bad username or password")

                self._logger.info("Login successful")

            self._connection = conn

            return conn
