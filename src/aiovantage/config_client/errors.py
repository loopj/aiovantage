import asyncio


class ClientError(Exception):
    pass


class ClientConnectionError(ClientError):
    pass


class ClientTimeoutError(asyncio.TimeoutError, ClientConnectionError):
    pass
