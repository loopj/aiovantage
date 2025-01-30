"""Connection to a Vantage Host Command service."""

import re

from typing_extensions import override

from aiovantage.connection import BaseConnection
from aiovantage.errors import LoginFailedError


class CommandConnection(BaseConnection):
    """Connection to a Vantage Host Command service."""

    default_port = 3001
    default_ssl_port = 3010

    @override
    async def post_open(self) -> None:
        self.authenticated = False
        self.requires_authentication = await self._requires_authentication()

        if not self.requires_authentication:
            self.supports_enhanced_log = await self._supports_enhanced_log()

    async def authenticate(self, username: str, password: str) -> None:
        """Authenticate the connection."""
        # Send the login command
        await self.write(f"LOGIN {username} {password}\n")

        # Check for errors
        response = await self.readuntil(b"\r\n")
        if response.startswith("R:ERROR"):
            raise LoginFailedError(response)

        self.authenticated = True
        self.supports_enhanced_log = await self._supports_enhanced_log()

    async def _requires_authentication(self) -> bool:
        """Check if the connection requires authentication."""
        if self.authenticated:
            return False

        # Send an ECHO command
        await self.write("ECHO\n")

        # If we get an error, we need to authenticate
        response = await self.readuntil(b"\r\n")
        if response.startswith("R:ERROR"):
            return True

        return False

    async def _supports_enhanced_log(self) -> bool:
        """Check if the connection supports enhanced log commands."""
        # Send the ELAGG command
        await self.write("ELAGG 1\n")

        # Check the response matches the expected format
        response = await self.readuntil(b"\r\n")
        if re.match(r"R:ELAGG 1 (ON|OFF)", response):
            return True

        return False
