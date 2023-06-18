"""Base class for command client interfaces."""

from typing import Union

from aiovantage.command_client import CommandClient, CommandResponse


class Interface:
    """Base class for command client object interfaces."""

    def __init__(self, client: CommandClient) -> None:
        """Initialize an object interface for standalone use.

        Args:
            client: The command client to use.
        """
        self._command_client = client

    @property
    def command_client(self) -> CommandClient:
        """Return the command client."""
        return self._command_client

    async def invoke(
        self, vid: int, method: str, *params: Union[int, float, str]
    ) -> CommandResponse:
        """Invoke a method on an object.

        Args:
            vid: The Vantage ID of the object to invoke the method on.
            method: The name of the method to invoke.
            params: The parameters to pass to the method.
        """
        return await self.command_client.command("INVOKE", vid, method, *params)
