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

from helpers import get_current_time, print_msg
from task import simple_task

executor = ProcessPoolExecutor(max_workers=10)


async def main():
    nc = NatsClient()
    sc = StanClient()
    print_msg('Client initiated')
    try:
        await nc.connect(servers=['nats://nats:4223'], io_loop=asyncio.get_running_loop())
        await sc.connect('test-cluster', f'simple_service_client_{ObjectId()}', nats=nc)
        print_msg('Connected to NATS')
    except ErrNoServers as e:
        print(e)
        return

    async def on_created(msg):
        subject = msg.sub
        data = msg.data.decode()
        body = json.loads(data)
        print(f"{get_current_time()}[PID: {os.getpid()}]  Received a message on '{subject} ': {data}")

        async def new_task(event_data: dict):
            res = await asyncio.get_running_loop().run_in_executor(executor, simple_task, event_data)
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>', res)
            await sc.publish('task:simple:finished', payload=b'{"test": "test"}')
            print('<<<<<<<<<<<<<<<<<<<<<<<<<<<')

        asyncio.create_task(new_task(body))

    await sc.subscribe("simple:created", cb=on_created, queue="simple.queue")
    print_msg('Subscribed to the simple:created channel')


if __name__ == '__main__':
    print_msg('Simple Service started...')
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print_msg('Interrupted by user')
        loop.stop()
        print_msg('Loop stopped user')
    finally:
        loop.close()
        print_msg('Loop closed')
