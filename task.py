#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from time import sleep

from helpers import print_msg


def simple_task(msg_body: dict):
    print_msg(f"[PID: {os.getpid()}]  Task started ({msg_body})")
    sleep(5)
    return 'azaza'

# executor = ProcessPoolExecutor()
#
# async def process(nats, data):
#     res = await asyncio.get_running_loop().run_in_executor(real_sync_process, data)
#     await nats.post(res)
#
# async def main():
#     nats = Nats()
#     while True:
#        data = nats.get()
#        asyncio.create_task(process(nats, data))
#
# if __name__=="__main__":
#     asyncio.run(main())
