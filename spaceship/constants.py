"""project global constants"""

import logging
import os

from utils import read_frames

TIC_TIMEOUT = 1 / 60  # 60 fps
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SPACESHIP_FRAMES_DIR = os.path.join(BASE_DIR, "frames", "spaceship")
SPACESHIP_FRAMES = read_frames(SPACESHIP_FRAMES_DIR)

EXPLOSION_FRAMES_DIR = os.path.join(BASE_DIR, "frames", "explosion")
EXPLOSION_FRAMES = read_frames(EXPLOSION_FRAMES_DIR)

OBSTACLES_FRAMES_DIR = os.path.join(BASE_DIR, "frames", "obstacles")
OBSTACLES_FRAMES = read_frames(OBSTACLES_FRAMES_DIR)

STARS = "+*.:"

DEBUG = False
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO

MIN_OBSTACLES_SPEED = .1
MAX_OBSTACLES_SPEED = .2
