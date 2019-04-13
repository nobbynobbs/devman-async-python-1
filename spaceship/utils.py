"""utils and helpers"""

import asyncio
import os
import random

from constants import TIC_TIMEOUT
from curses_tools import read_controls

async def sleep(seconds):
    """asyncio.sleep(0) wrapper"""
    for _ in range(int(seconds // TIC_TIMEOUT) or 1):
        await asyncio.sleep(0)


def get_canvas_center(canvas):
    """return tuple `(row, column)`"""
    height, width = canvas.getmaxyx()
    return height // 2, width // 2


def read_frames(frames_dir):
    """read all frame files from directory into list of strings"""
    frames = []
    for filename in os.listdir(frames_dir):
        with open(os.path.join(frames_dir, filename)) as f_d:
            frames.append(f_d.read())
    return frames


def get_random_coordinates_list(canvas, low=50, high=100):
    """generate the list of tuples with random coordnates inside canvas"""
    count = random.randint(low, high)
    height, width = canvas.getmaxyx()
    return [
        (random.randint(1, height - 2), random.randint(1, width - 2))
        for _ in range(count)
    ]


async def handle_inputs(ship, canvas):
    """async wrapper for controls handler"""
    while True:
        row, column, shoot = read_controls(canvas)  # non-blocking
        await ship.move(canvas, row, column)
        if shoot:
            ship.shoot(canvas)
