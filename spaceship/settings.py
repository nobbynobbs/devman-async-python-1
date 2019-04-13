"""application settings"""

import logging

DEBUG = False
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO

MIN_OBSTACLES_SPEED = .1
MAX_OBSTACLES_SPEED = .2
