"""project global constants"""

import os

# event loop frequency ~60hz
TIC_TIMEOUT = 1 / 60

# project root directory
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# frames directories
SPACESHIP_FRAMES_DIR = os.path.join(BASE_DIR, "frames", "spaceship")
EXPLOSION_FRAMES_DIR = os.path.join(BASE_DIR, "frames", "explosion")
GARBAGE_FRAMES_DIR = os.path.join(BASE_DIR, "frames", "obstacles")

# stars symbols
STARS = "+*.:"
