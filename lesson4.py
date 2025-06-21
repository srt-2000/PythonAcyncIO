import asyncio


async def coro(message):
    print(message)
    await asyncio.sleep(1)
    print('second\n' + message)


async def main():
    print('-- main beginning --')

    asyncio.create_task(coro('coro message'))
    print(asyncio.all_tasks())

    await asyncio.sleep(0.5)  # 0.5 < 1 and second message will not print, because main faster and run will close it first

    print('-- main done --')

asyncio.run(main())