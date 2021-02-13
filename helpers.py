#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime


def get_current_time():
    return datetime.now().strftime('[%d %b %Y %H:%M:%S]    ')


def print_msg(msg: str) -> None:
    print(f'{get_current_time()}{msg}')
