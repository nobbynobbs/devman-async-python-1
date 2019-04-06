import asyncio
import os
import random

from constants import TIC_TIMEOUT, BASE_DIR


async def sleep(seconds):
    for _ in range(int(seconds // TIC_TIMEOUT)):
        await asyncio.sleep(0)

def canvas_center(canvas):
    """return tuple `(row, column)`"""
    height, width = canvas.getmaxyx()
    return height // 2, width // 2

def read_frames():
    frames_dir = os.path.join(BASE_DIR, "frames")
    return [open(os.path.join(frames_dir, f)).read() for f in os.listdir(frames_dir)]


def random_coordinates_list(canvas, min=50, max=100):
    count = random.randint(min, max)
    height, width = canvas.getmaxyx()
    return [
        (random.randint(1, height - 2), random.randint(1, width - 2))
        for _ in range(count)
    ]
