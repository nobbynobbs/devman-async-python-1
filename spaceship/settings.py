"""application settings"""

import logging

DEBUG = True
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO

MIN_OBSTACLES_SPEED = 0.1
MAX_OBSTACLES_SPEED = 0.2

YEAR_IN_SECONDS = 5
SPACE_ERA_BEGINNING = 1957
