import asyncio
from asyncio import timeout
from random import randint


class C:
    norm = '\033[0m'
    blue = '\033[94m'
    green = '\033[92m'

c = C()

async def producer(queue, name):
    timeout = randint(1,5)
    await queue.put(timeout)
    print(f'{c.blue}Producer {name} put {timeout} to the queue, {queue}{c.norm}')


async def consumer(queue, name):
    while True:                        # not queue.empty():
        timeout = await queue.get()
        await asyncio.sleep(timeout)
        print(f'{c.green}Consumer ate {timeout}, {queue}{c.norm}')
        queue.task_done()


async def main():
    queue = asyncio.Queue(maxsize=3)

    producers = []
    for i in range(12):
        task = asyncio.create_task(producer(queue, name=i))
        producers.append(task)

    consumers = []
    for i in range(4):
        task = asyncio.create_task(consumer(queue, name=i))
        consumers.append(task)

    await asyncio.gather(*producers)
    await queue.join()



asyncio.run(main())

