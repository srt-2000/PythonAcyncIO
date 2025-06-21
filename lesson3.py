import asyncio
import inspect

# async def coro():
#     return 1
#
# async def main():
#     mytask = asyncio.create_task(coro())
#
#     await mytask
#     print(mytask.done())
#     print(mytask.cancelled())
#
# asyncio.run(main())

# async def f():
#     return 1
#
# async def greet(timeout):
#     await asyncio.sleep(timeout)
#     return 'BBQ'
#
# async def f_main():
#     await asyncio.sleep(3) #f_main stop, sleep start
#     return 123 # f_main start
#
# async def greet_main():
#     # in this realisation res1 and res2 will print async and res1 without sleep(5)!!!
#     print('start bbq')
#     res1 = asyncio.create_task(f()) #its task object
#     res2 = asyncio.create_task(greet(2)) #its task object
#     res3 = asyncio.create_task(greet(20)) #its task object
#     res4 = asyncio.create_task(greet(4)) #its task object
#     res5 = asyncio.create_task(greet(6)) #its task object
#
#     print(await res1)
#     print(await res2)
#     print(await res3)
#     print(await res4)
#     print(await res5)
#
# asyncio.run(greet_main())

# async def greet(timeout):
#     await asyncio.sleep(timeout)
#     return 'BBQ'
#
# async def greet_main():
#     long_task = asyncio.create_task(greet(60)) #its task object
#     seconds = 0
#
#     while not long_task.done():
#         await asyncio.sleep(1)
#         seconds += 1
#
#         if seconds == 5:
#             long_task.cancel()
#         print('Time passed', seconds)
#
#     try:
#         await long_task
#     except asyncio.CancelledError:
#         print('long_task CANCELLED')
#
# asyncio.run(greet_main())

# async def greet(timeout):
#     await asyncio.sleep(timeout)
#     return 'BBQ'
#
# async def greet_main():
#     long_task = asyncio.create_task(greet(60)) #its task object
#
#     try:
#         result = await asyncio.wait_for(long_task, timeout=5)
#     except asyncio.TimeoutError:
#         print('long_task CANCELLED')
#
# asyncio.run(greet_main())


async def greet(timeout):
    await asyncio.sleep(timeout)
    return 'BBQ'

async def greet_main():
    long_task = asyncio.create_task(greet(6)) #its task object

    try:
        result = await asyncio.wait_for(
            asyncio.shield(long_task),
            timeout=2
        )
    except asyncio.TimeoutError:
        print('long_task IN PROCESS')
        result = await long_task
        print(result)

asyncio.run(greet_main())
