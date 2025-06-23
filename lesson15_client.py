import asyncio
import time
import aiohttp


lock = asyncio.Lock()

async def make_request(url):
    async with aiohttp.ClientSession() as session:
        async with lock:
            async with session.get(url) as response:
                data = await response.json()
                print(data)

                await asyncio.sleep(0.5)


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

    wo_lock_tasks = [
        asyncio.create_task(without_lock('http://localhost:8000/hello'))
        for i in range(3)
    ]

    await asyncio.gather(*tasks, *wo_lock_tasks)

    print(time.monotonic() - start)


asyncio.run(main())