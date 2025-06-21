import asyncio
import aiohttp


async def coro_norm():
    return 'halohalo'


async def coro_value_error():
    raise ValueError


async def coro_type_error():
    raise TypeError



async def coro_long():
    try:
        print('Long task starts...')
        await asyncio.sleep(3)
        print("Long task done")
        return 'Long task RETURNING'
    except asyncio.CancelledError as e:
        print('All needed actions done')
        raise asyncio.CancelledError


async def main():

    try:
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(coro_norm())
            task2 = tg.create_task(coro_value_error())
            task3 = tg.create_task(coro_long(), name='COROCOROLONGLONG')

        results = [task1.result(), task2.result(), task3.result()]
        print(results)
    except* ValueError as e:
        print(f'{e=}')


# async def main():
#
#     task1 = asyncio.create_task(coro_norm())
#     task2 = asyncio.create_task(coro_value_error())
#     task3 = asyncio.create_task(coro_long(), name = 'COROCOROLONGLONG')
#
#     tasks = [task1, task2, task3]
#
#     try:
#         results = await asyncio.gather(*tasks)
#     except ValueError as e:
#         print(f'{e=}')
#     else:
#         print(f'{results=}')
#
#     for task in tasks:
#         if not task.done():
#             task.cancel()
#             print(f'Pending: {task.get_name()}')
#
#     print()
#
#     await asyncio.sleep(3)
#     print(task1._state)
#     print(task2._state)
#     print(task3._state)


asyncio.run(main())