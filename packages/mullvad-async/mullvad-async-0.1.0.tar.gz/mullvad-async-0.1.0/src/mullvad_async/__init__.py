from typing import Optional

import aiohttp
from .const import MULLVAD_API_ACCOUNT, MULLVAD_API_CONNECTED


class Mullvad:
    """
    An object that requests data from Mullvad's API.
    """

    def __init__(self, session: aiohttp.ClientSession, user: Optional[str] = None):
        self._session = session
        self._user = user

    async def _request(self, url: str) -> dict:
        async with self._session.get(url) as resp:
            json = await resp.json()

            # Error check
            if "code" in json:
                detail = json.get(
                    "detail", f"Request rejected for reason {json['code']}"
                )
                raise MullvadAPIError(detail)

            return json

    async def account_status(self) -> dict:
        if self._user is None:
            raise MullvadAPIError("User account was not specified.")
        else:
            return await self._request(MULLVAD_API_ACCOUNT + self._user)

    async def is_connected(self) -> dict:
        return await self._request(MULLVAD_API_CONNECTED)


class MullvadAPIError(Exception):
    """Failed to fetch Mullvad API data."""

    pass
