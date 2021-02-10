#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import json
import os
from concurrent.futures import ProcessPoolExecutor

from bson import ObjectId
from nats.aio.client import Client as NatsClient
from nats.aio.errors import ErrNoServers
from stan.aio.client import Client as StanClient

from helpers import get_current_time
from task import simple_task


async def run(async_loop):
    nc = NatsClient()
    sc = StanClient()

    try:
        await nc.connect(servers=['nats://localhost:4223'], io_loop=async_loop)
        await sc.connect('test-cluster', f'simple_service_client_{ObjectId()}', nats=nc)
    except ErrNoServers as e:
        print(e)
        return
    executor = ProcessPoolExecutor(max_workers=4)

    async def on_created(msg):
        subject = msg.sub
        data = msg.data.decode()
        print(f"{get_current_time()}[PID: {os.getpid()}]  Received a message on '{subject} ': {data}")

        async def new_task(event_data):
            body = json.loads(event_data)
            await async_loop.run_in_executor(executor, simple_task, body)

        asyncio.create_task(new_task(data))

    await sc.subscribe("simple:created", cb=on_created, queue="simple.queue")


def main():
    async_loop = asyncio.get_event_loop()
    async_loop.run_until_complete(run(async_loop))
    try:
        async_loop.run_forever()
    except KeyboardInterrupt:
        async_loop.stop()
    finally:
        async_loop.close()


if __name__ == '__main__':
    print(f'{get_current_time()}BIM Data Service...')
    print(f'{get_current_time()}Schema Validation Worker started:')
    main()
