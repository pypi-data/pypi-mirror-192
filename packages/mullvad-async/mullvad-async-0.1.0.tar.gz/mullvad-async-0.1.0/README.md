# Mullvad Async API Library

This is a very simple library to pull down information from Mullvad's unofficial API using your account number. This information includes:
- Account status
- Number of clients
- Client information
- If currently connected to Mullvad VPN

An example of simple usage is
```
from mullvad_async import Mullvad
import asyncio

    async def main():
        async with aiohttp.ClientSession() as session:
            mullvad = Mullvad(session, "my_account")

            connected = await mullvad.is_connected()
            
            account = await mullvad.account_status()
            print(account["account"]["active"])

    asyncio.run(main())
```

To install run
```
pip install mullvad-async
```