#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import os

from bson import ObjectId
from nats.aio.client import Client as NatsClient
from nats.aio.errors import ErrNoServers
from stan.aio.client import Client as StanClient

from helpers import get_current_time


async def get_sc():
    nc = NatsClient()
    sc = StanClient()

    try:
        await nc.connect(servers=['nats://nats:4223'])
        await sc.connect('test-cluster', f'simple_service_client_{ObjectId()}', nats=nc)
    except ErrNoServers as e:
        print(e)
        return
    return sc


async def pub(channel, payload):
    print('########################################### TEST ##########################################################')
    sc = await get_sc()
    await sc.publish(channel, payload=payload)


def simple_task(msg_body: dict):
    print(f"{get_current_time()}[PID: {os.getpid()}]  Task started ({msg_body})")

    async_loop = asyncio.get_event_loop()
    async_loop.run_until_complete(pub('task:simple:started', b'{"test": "test"}'))

