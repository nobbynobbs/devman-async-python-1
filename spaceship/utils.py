"""utils and helpers"""

import os
import random


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


def rand(left, right):
    """random number from interval [left, right]"""
    return left + (random.random() * (right - left))
