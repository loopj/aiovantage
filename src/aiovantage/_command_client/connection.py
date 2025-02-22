import re

from typing_extensions import override

from aiovantage._connection import BaseConnection
from aiovantage.errors import ClientConnectionError, LoginFailedError

from .converter import Converter


class CommandConnection(BaseConnection):
    """Connection to a Vantage Host Command service."""

    default_port = 3001
    default_ssl_port = 3010

    @property
    def authenticated(self) -> bool:
        """Check if the connection is authenticated."""
        if self.closed:
            raise ClientConnectionError("Client not connected")

        return self._authenticated

    @property
    def requires_authentication(self) -> bool:
        """Check if the connection requires authentication."""
        if self.closed:
            raise ClientConnectionError("Client not connected")

        return self._requires_authentication

    @property
    def supports_enhanced_log(self) -> bool:
        """Check if the connection supports enhanced log commands."""
        if self.closed:
            raise ClientConnectionError("Client not connected")

        return self._supports_enhanced_log

    async def authenticate(self, username: str, password: str) -> None:
        """Authenticate the connection.

        Args:
            username: The username to use for authentication.
            password: The password to use for authentication.
        """
        if self.closed:
            raise ClientConnectionError("Client not connected")

        # Send the login command
        await self.write(
            f"LOGIN {Converter.serialize(username)} {Converter.serialize(password)}\n"
        )

        # Check for errors
        response = await self.readuntil(b"\r\n")
        if response.startswith("R:ERROR"):
            raise LoginFailedError(response)

        self._authenticated = True
        self._supports_enhanced_log = await self._get_supports_enhanced_log()

    @override
    async def open(self) -> None:
        await super().open()

        self._authenticated = False
        self._requires_authentication = await self._get_requires_authentication()

        if not self._requires_authentication:
            self._supports_enhanced_log = await self._get_supports_enhanced_log()

    async def _get_requires_authentication(self) -> bool:
        if self.authenticated:
            return False

        # Send an ECHO command
        await self.write("ECHO\n")

        # If we get an error, we need to authenticate
        response = await self.readuntil(b"\r\n")
        if response.startswith("R:ERROR"):
            return True

        return False

    async def _get_supports_enhanced_log(self) -> bool:
        # Send the ELAGG command
        await self.write("ELAGG 1\n")

        # Check the response matches the expected format
        response = await self.readuntil(b"\r\n")
        match = re.search(r"R:ELAGG 1 (ON|OFF)", response)
        if match:
            return match.group(1) == "ON"

        return False
