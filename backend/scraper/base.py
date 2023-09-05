import asyncio
from abc import ABC
from json import loads
import aiohttp
from utils.headers import get_headers
import logging
from random import choice
from typing import Tuple
from multidict import CIMultiDictProxy


class Scraper(ABC):
    session: aiohttp.ClientSession = None
    api_url: str = None

    @classmethod
    async def set_session(cls):
        if not cls.session:
            cls.session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.session:
            await self.session.close()

    @classmethod
    async def get_api(cls, data: dict, headers: dict = get_headers()) -> dict:
        return loads(await cls.get(cls.api_url, data, headers))

    @classmethod
    async def get(cls, url: str, data=None, headers: dict = get_headers()) -> str:
        if not cls.session:
            await Scraper.set_session()

        data = {} or data
        err, tries = None, 0

        while tries < 10:
            try:
                async with cls.session.get(url=url, params=data, headers=headers) as resp:
                    if resp.status != 200:
                        err = f"request failed with status: {resp.status}\n err msg: {resp.content}"
                        logging.error(f"{err}\nRetrying...")
                        raise aiohttp.ClientResponseError(None, None, message=err)

                    return await resp.text()
            except (aiohttp.ClientOSError, asyncio.TimeoutError, aiohttp.ServerDisconnectedError, aiohttp.ServerTimeoutError):
                await asyncio.sleep(choice([5, 4, 3, 2, 1]))  # randomly await
                tries += 1
                continue

        raise aiohttp.ClientResponseError(None, None, message=err)


class Proxy(Scraper):
    @classmethod
    async def get(cls, url: str, data=None, headers=None) -> Tuple[bytes, CIMultiDictProxy[str]]:
        if headers is None:
            headers = get_headers()

        if not cls.session:
            await Proxy.set_session()

        data = {} or data
        err, tries = None, 0

        while tries < 5:
            try:
                async with cls.session.get(url=url, params=data, headers=headers) as resp:
                    if resp.status != 200:
                        err = f"request failed with status: {resp.status}\n err msg: {resp.content}"
                        logging.error(f"{err}\nRetrying...")
                        raise aiohttp.ClientResponseError(None, None, message=err)

                    return await resp.read(), resp.headers
            except (aiohttp.ClientOSError, asyncio.TimeoutError, aiohttp.ServerDisconnectedError, aiohttp.ServerTimeoutError):
                await asyncio.sleep(choice([5, 4, 3, 2, 1]))  # randomly await
                tries += 1
                continue

        raise aiohttp.ClientResponseError(None, None, message=err)