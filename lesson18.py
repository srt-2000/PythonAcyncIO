import asyncio
from asyncio import gather
from random import randint


async def waiter(condition, id):
    async with condition:
        print(f'Waiter {id} is awaiting')
        await condition.wait()

        num = randint(1, 6)
        print(f'Waiter {id} generated {num}')


async def starter(condition):
    print('Starter is waiting for 5 sec')
    await asyncio.sleep(5)

    async with condition:
        # condition.notify_all()
        condition.notify(2)



async def main():
    condition = asyncio.Condition()

    waiters = [
        asyncio.create_task(
            waiter(condition, id=i)
        ) for i in range(6)
    ]

    await asyncio.create_task(starter(condition))
    await asyncio.gather(*waiters)

asyncio.run(main())
