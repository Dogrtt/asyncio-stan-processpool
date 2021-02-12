#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import json

from bson import ObjectId
from nats.aio.client import Client as NatsClient
from nats.aio.errors import ErrNoServers
from stan.aio.client import Client as StanClient


async def run(async_loop):
    nc = NatsClient()
    sc = StanClient()

    try:
        await nc.connect(servers=['nats://localhost:4223'], io_loop=async_loop)
        await sc.connect('test-cluster', f'simple_service_client_{ObjectId()}', nats=nc)
    except ErrNoServers as e:
        print(e)
        return
    for i in range(1):
        message = json.dumps({"simple": f"simple_{i}"})
        await sc.publish('simple:created', bytes(message.encode('utf-8')))


if __name__ == '__main__':
    async_loop = asyncio.get_event_loop()
    async_loop.run_until_complete(run(async_loop))
