"""Connection to a Vantage Host Command service."""

import re

from aiovantage.connection import BaseConnection
from aiovantage.errors import LoginFailedError


class CommandConnection(BaseConnection):
    """Connection to a Vantage Host Command service."""

    default_port = 3001
    default_ssl_port = 3010

    _authenticated = False
    _supports_enhanced_log = False

    async def authenticate(self, username: str, password: str) -> None:
        """Authenticate the connection."""
        # Send the login command
        await self.write(f"LOGIN {username} {password}\n")

        # Check for errors
        response = await self.readuntil(b"\r\n")
        if response.startswith("R:ERROR"):
            raise LoginFailedError(response)

        self._authenticated = True

    async def populate_capabilities(self) -> None:
        """Populate the capabilities of the connection."""
        # Send the ELAGG command
        await self.write("ELAGG 1\n")

        # Check the response matches the expected format
        response = await self.readuntil(b"\r\n")
        if re.match(r"R:ELAGG 1 (ON|OFF)", response):
            self._supports_enhanced_log = True

    @property
    def authenticated(self) -> bool:
        """Return whether the connection is authenticated."""
        return self._authenticated

    @property
    def supports_enhanced_log(self) -> bool:
        """Return whether the connection supports the enhanced log."""
        return self._supports_enhanced_log
