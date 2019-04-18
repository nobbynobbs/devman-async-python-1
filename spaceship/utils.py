"""utils and helpers"""

import os
import random

from core.constants import (
    SPACESHIP_FRAMES_DIR,
    EXPLOSION_FRAMES_DIR,
    GARBAGE_FRAMES_DIR,
    BASE_DIR,
)


def read_all_frames():
    """read frames from files"""
    frames = {
        "spaceship": read_frames(SPACESHIP_FRAMES_DIR),
        "explosion": read_frames(EXPLOSION_FRAMES_DIR),
        "garbage": read_frames(GARBAGE_FRAMES_DIR),
    }
    with open(os.path.join(BASE_DIR, "frames", "gameover.txt")) as f_d:
        frames["gameover"] = f_d.read()
    return frames


def read_frames(frames_dir):
    """read all frame files from directory into list of strings"""
    frames = []
    for filename in sorted(os.listdir(frames_dir)):
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


def rand(left, right):
    """random number from interval [left, right]"""
    return left + (random.random() * (right - left))
