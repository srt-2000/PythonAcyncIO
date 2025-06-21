import asyncio
from redis import asyncio as aioredis

class A:
    def __iter__(self):
        self.x = 0
        return self

    def __next__(self):
        if self.x > 2:
            raise StopIteration
        else:
            self.x += 1
            return self.x

class RedisReader:
    def __init__(self, redis, keys):
        self.redis = redis
        self.keys = keys

    def __aiter__(self):
        self.ikeys = iter(self.keys)
        return self

    async def __anext__(self):
        try:
            key = next(self.ikeys)
        except StopIteration:
            raise StopAsyncIteration

        async with self.redis.client() as connection:
            name = await connection.get(key)

        return name


async def main():
    redis = await aioredis.from_url('redis://localhost')

    keys = ['molchanov', 'ivanov', 'petrov', 'vader']

    async for name in RedisReader(redis, keys):
        print(name)


asyncio.run(main())