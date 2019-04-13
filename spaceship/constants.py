"""project global constants"""

import logging
import os

TIC_TIMEOUT = 1 / 60  # 60 fps
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPACESHIP_FRAMES_DIR = os.path.join(BASE_DIR, "frames/spaceship")
STARS = "+*.:"

DEBUG = False
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO
