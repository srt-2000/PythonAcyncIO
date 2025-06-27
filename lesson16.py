import asyncio
import time
import aiohttp


semaphore = asyncio.Semaphore(4)

async def make_request(url):
    async with aiohttp.ClientSession() as session:
        async with semaphore:
            async with session.get(url) as response:
                data = await response.json()
                print(data)

                await asyncio.sleep(0.5)

                print('-----------')


async def without_lock(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            print(data)


async def get_data(url):
    await make_request(url)


async def main():
    start = time.monotonic()

    tasks = [
        asyncio.create_task(get_data('http://localhost:8000'))
        for i in range(20)
    ]


    await asyncio.gather(*tasks,)

    print(time.monotonic() - start)


asyncio.run(main())