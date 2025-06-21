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
        return f'{url}: {html[:20]}'


async def coro_norm():
    return 'halohalo'


async def coro_value_error():
    raise ValueError


async def coro_type_error():
    raise TypeError


async def main():
    try:
        results = await asyncio.gather(
            coro_norm(),
            coro_value_error(),
            coro_type_error(),
        )

    except ValueError as e:
        print(f'{e=}')
    except TypeError as e:
        print(f'{e=}')
    else:
        print(f'{results=}')

    # async with asyncio.TaskGroup() as tg:
    #     print(type(tg))
    #     print(dir(tg))
    #     print()
    #
    #     res1 = tg.create_task(check('https://yandex.ru'))
    #     res2 = tg.create_task(check('https://google.com'))
    #     res3 = tg.create_task(check('https://mail.ru'))
    #
    # print(res1.result())
    # print(res2.result())
    # print(res3.result())

asyncio.run(main())