import asyncio
import aiohttp


#async session with context manager
class AsyncSession:
    def __init__(self, url):
        self._url = url

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        response = await self.session.get(self._url)
        return response

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()


async def check(url):
    async with AsyncSession(url) as response:
        html = await response.text()
        print(f'{url}: {html[:20]}')

# async def main():
#     await asyncio.create_task(check('https://yandex.ru'))
#     await asyncio.create_task(check('https://google.com'))
#     await asyncio.create_task(check('https://farpost.ru'))

async def main():
    res1 = asyncio.create_task(check('https://yandex.ru'))
    res2 = asyncio.create_task(check('https://google.com'))
    res3 = asyncio.create_task(check('https://farpost.ru'))

    print(await res1)
    print(await res2)
    print(await res3)

asyncio.run(main())