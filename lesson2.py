import asyncio
import inspect

async def f():
    return 1

async def greet():
    await asyncio.sleep(5)
    return 'BBQ'

async def f_main():
    await asyncio.sleep(3) #f_main stop, sleep start
    return 123 # f_main start

async def greet_main():
    # in this realisation res1 and res2 will print sync - together!!!
    print('start bbq')
    res1 = await f() #its coroutine
    res2 = await greet() #its coroutine

    print(res1)
    print(res2)

coro = f()
print(coro)
print(type(coro))
print(inspect.iscoroutine(coro))
print(asyncio.run(coro))

print(asyncio.run(f_main()))
asyncio.run(greet_main())