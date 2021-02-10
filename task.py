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
        await nc.connect(servers=['nats://localhost:4223'], io_loop=asyncio.get_event_loop())
        await sc.connect('test-cluster', f'simple_service_client_{ObjectId()}', nats=nc)
    except ErrNoServers as e:
        print(e)
        return
    print('CONNECTED!')
    return sc

def simple_task(msg_body: dict):
    async def pub(channel, payload):
        print('PUB_0')
        sc = await get_sc()
        print('PUB_1')
        await sc.publish(channel, payload=payload)
        print('PUB_2')

    print(f"{get_current_time()}[PID: {os.getpid()}]  Task started ({msg_body})")
    asyncio.create_task(pub('task:simple:started', b'{"test": "test"}'))
