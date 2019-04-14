"""project global constants"""

import os

from utils import read_frames

TIC_TIMEOUT = 1 / 60  # 60 fps
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# maybe FIXME: reading frames in import time. I doubt if it's good idea.
SPACESHIP_FRAMES_DIR = os.path.join(BASE_DIR, "frames", "spaceship")
SPACESHIP_FRAMES = read_frames(SPACESHIP_FRAMES_DIR)

EXPLOSION_FRAMES_DIR = os.path.join(BASE_DIR, "frames", "explosion")
EXPLOSION_FRAMES = read_frames(EXPLOSION_FRAMES_DIR)

OBSTACLES_FRAMES_DIR = os.path.join(BASE_DIR, "frames", "obstacles")
OBSTACLES_FRAMES = read_frames(OBSTACLES_FRAMES_DIR)

with open(os.path.join(BASE_DIR, "frames", "gameover.txt")) as f_d:
    GAMEOVER_FRAME = f_d.read()

STARS = "+*.:"
