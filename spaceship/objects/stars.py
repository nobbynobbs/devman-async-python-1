"""stars generator and render"""

import curses
import random

from core.constants import STARS
from core.loop import sleep
from utils import get_random_coordinates_list, rand

def get_stars_coroutines(canvas):
    """return list of blinking coroutines"""
    return [
        blink(canvas, row, column, random.choice(STARS), rand(0, 1))
        for row, column in get_random_coordinates_list(canvas)
    ]


async def blink(canvas, row, column, symbol="*", delay=0):
    """twinkle twinkle little star"""
    await sleep(delay)
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(2)

        canvas.addstr(row, column, symbol)
        await sleep(0.3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(0.5)

        canvas.addstr(row, column, symbol)
        await sleep(0.3)
