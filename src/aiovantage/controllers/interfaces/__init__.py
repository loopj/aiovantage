from typing import Union

from aiovantage.command_client import CommandClient, CommandResponse


class Interface:
    command_client: CommandClient

    async def invoke(self, id: int, *params: Union[int, float, str]) -> CommandResponse:
        """
        Invoke a command on an object.

        Args:
            id: The ID of the object.
            args: The arguments to pass to the command.
        """

        return await self.command_client.command("INVOKE", id, *params)
