import asyncio


async def busy_loop():
    for i in range(10):
        await nothing()


async def nothing():
    # we need sleep(0) to use nothing and normal async
    # - if not we will have normal after nothing
    # - because coroutines will give result immediately
    await asyncio.sleep(0)
    print('nothing')


async def normal():
    for i in range(10):
        await asyncio.sleep(0) # we need sleep(0) to use nothing and normal async
        print('normal coroutine')


async def main():
    # await asyncio.create_task(busy_loop())
    ## - in this var - await will block parent coroutine busy_loop
    ## - and we will have normal after nothing
    # await asyncio.create_task(normal())
    await asyncio.gather(
        busy_loop(),
        normal()
    )


asyncio.run(main())