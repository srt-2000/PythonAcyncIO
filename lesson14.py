# async crawler (queue parser)
"""
https://xkcd.com
"""

import asyncio
import aiohttp
import aiofiles

from concurrent.futures import ProcessPoolExecutor
from bs4 import BeautifulSoup

async def make_request(url, session):
    response = await session.get(url)

    if response.ok:
        return response
    else:
        print(f'{url} returned: {response.status}')


async def get_image_page(queue, session):
    url = 'https://c.xkcd.com/random/comic/'
    response = await make_request(url, session)
    await queue.put(response.url)


def _parse_link(html):
    soup = BeautifulSoup(html, 'lxml')
    image_link = 'https:' + soup.select_one('div#comic>img').get('src')
    return image_link


async def get_image_url(pages_queue, image_urls_queue, session):
    while True:
        url = await pages_queue.get()
        response = await make_request(url, session)
        html = await response.text()

        loop = asyncio.get_running_loop()
        with ProcessPoolExecutor() as pool:
            image_link = await loop.run_in_executor(pool, _parse_link, html)

        await image_urls_queue.put(image_link)

        pages_queue.task_done()


async def download_image(queue, session):
    while True:
        url = await queue.get()
        response = await make_request(url, session)
        filename = url.split('/')[-1]
        async with open(filename, 'wb') as f:
            async for chunk in response.content.iter_chunked(1024):
                await f.write(chunk)

        queue.task_done()

def cancel_tasks(tasks):
    [task.cancel() for task in tasks]    # refactoring of repeatable code


def create_tasks(number_of_workers, coro, *args):
    tasks = []
    for _ in range(number_of_workers):
        task = asyncio.create_task(coro(*args))
        tasks.append(task)
    return tasks


async def main():
    session = aiohttp.ClientSession()
    pages_queue = asyncio.Queue()
    image_url_queue = asyncio.Queue()

    page_getters = create_tasks(4, get_image_page, pages_queue, session) # create a list of asyncio task objects
    # page_getters = []
    # for i in range(4):
    #     task = asyncio.create_task(get_image_page(pages_queue, session)) # without await because we need task object only
    #     page_getters.append(task)

    url_getters = create_tasks(4, get_image_url, pages_queue, image_url_queue, session) # create a list of asyncio task objects
    # url_getters = []  # create a list of asyncio task objects
    # for i in range(4):
    #     task = asyncio.create_task(
    #         get_image_url(pages_queue, image_url_queue, session))  # without await because we need task object only
    #     url_getters.append(task)

    downloaders = create_tasks(4, download_image, image_url_queue, session)  # create a list of asyncio task objects
    # downloaders = []  # create a list of asyncio task objects
    # for i in range(4):
    #     task = asyncio.create_task(download_image(image_url_queue, session))  # without await because we need task object only
    #     downloaders.append(task)

    await asyncio.gather(*page_getters)

    await pages_queue.join()   # because we need wait when all queue will be empty, not earlier
    cancel_tasks(page_getters)
    # for task in page_getters:  # delete all running but idle tasks
    #     task.cancel()

    await image_url_queue.join()   # because we need wait when all queue will be empty, not earlier
    cancel_tasks(downloaders)
    # for task in downloaders:  # delete all running but idle tasks
    #     task.cancel()

    await session.close() # we have to use context manager WITH... but we want to avoid session closing earlier as we need


asyncio.run(main())