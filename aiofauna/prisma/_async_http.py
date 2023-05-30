from typing import Any

import aiohttp

from ._types import Method
from .http_abstract import AbstractResponse, AbstractHTTP, ASYNC_DEFAULT_CONFIG


__all__ = ('HTTP', 'Response', 'client')


class HTTP(AbstractHTTP[aiohttp.ClientSession, aiohttp.ClientResponse]):
    session: aiohttp.ClientSession
    session_kwargs = ASYNC_DEFAULT_CONFIG
    __slots__ = ()

    async def download(self, url: str, dest: str) -> None:
        async with self.session.get(url) as resp:
            resp.raise_for_status()
            with open(dest, 'wb') as fd:
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break
                    fd.write(chunk)

    async def request(
        self, method: Method, url: str, **kwargs: Any
    ) -> 'Response':
        async with self.session.request(method, url, **kwargs) as resp:
            return Response(resp)
        
    def open(self) -> None:
        self.session = aiohttp.ClientSession(**self.session_kwargs)
        
    async def close(self) -> None:
        if self.should_close():
            await self.session.close()
            self.session = None # type: ignore[assignment]


client: HTTP = HTTP()


class Response(AbstractResponse[aiohttp.ClientResponse]):
    __slots__ = ()

    @property
    def status(self) -> int:
        return self.status

    async def json(self, **kwargs: Any) -> Any:
        return await self.original.json(**kwargs)

    async def text(self, **kwargs: Any) -> str:
        return await self.original.text(**kwargs)