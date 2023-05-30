from typing import Union
from aiovantage.command_client import CommandClient, CommandResponse


class Interface:
    def __init__(self, client: CommandClient) -> None:
        self._command_client = client

    @property
    def command_client(self) -> CommandClient:
        return self._command_client

    async def invoke(
        self, id: int, command: str, *params: Union[int, float, str]
    ) -> CommandResponse:
        return await self.command_client.command("INVOKE", id, command, *params)
