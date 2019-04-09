"""project global constants"""

import os

TIC_TIMEOUT = 1 / 60  # 60 fps
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPACESHIP_FRAMES_DIR = os.path.join(BASE_DIR, "frames")
STARS = "+*.:"
