import asyncio
import os
import random

from constants import TIC_TIMEOUT, BASE_DIR
from curses_tools import read_controls

async def sleep(seconds):
    for _ in range(int(seconds // TIC_TIMEOUT)):
        await asyncio.sleep(0)

def canvas_center(canvas):
    """return tuple `(row, column)`"""
    height, width = canvas.getmaxyx()
    return height // 2, width // 2

def read_frames(frames_dir):
    frames = []
    for filename in os.listdir(frames_dir):
        with open(os.path.join(frames_dir, filename)) as fd:
            frames.append(fd.read())
    return frames
    

def random_coordinates_list(canvas, min=50, max=100):
    count = random.randint(min, max)
    height, width = canvas.getmaxyx()
    return [
        (random.randint(1, height - 2), random.randint(1, width - 2))
        for _ in range(count)
    ]


async def handle_inputs(ship, canvas):
    while True:
        row, column, _ = read_controls(canvas)  # non-blocking
        ship.move(row, column, canvas)
        await asyncio.sleep(0)
