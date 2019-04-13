"""naive event loop implementation"""

import asyncio
import time

from constants import TIC_TIMEOUT


def run(canvas, coroutines):
    """invoke coroutines, collect exhausted coroutines"""
    while coroutines:
        # is it ok to allocate new set on each iteration?
        finished_coroutines = set()
        for coro in coroutines:
            try:
                coro.send(None)
            except StopIteration:
                finished_coroutines.add(coro)
        canvas.refresh()
        for coro in finished_coroutines:
            coroutines.remove(coro)
        time.sleep(TIC_TIMEOUT)  # limit event-loop frequency
        canvas.border()


async def sleep(seconds):
    """asyncio.sleep(0) wrapper"""
    for _ in range(int(seconds // TIC_TIMEOUT) or 1):
        await asyncio.sleep(0)