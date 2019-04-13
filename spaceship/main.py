#!/usr/bin/env python3

"""event loop and entry point"""

import curses
import logging
import os
import random
import uuid

import core.loop as loop
from animations import blink, fly_garbage
from constants import (
    STARS, BASE_DIR, LOG_LEVEL, DEBUG, OBSTACLES_FRAMES
)
from curses_tools import get_frame_size
from state import coroutines, obstacles
from obstacles import Obstacle, show_obstacles
from ship import Ship
from utils import (
    get_random_coordinates_list,
    get_canvas_center,
    handle_inputs,
    rand,
)


async def fill_orbit_with_garbage(canvas):
    """generates infinite garbage frames"""
    _, canvas_width = canvas.getmaxyx()
    if DEBUG:
        coroutines.append(show_obstacles(canvas, obstacles))
    while True:
        await loop.sleep(random.random() * 2)  # sleep [0, 2] seconds
        frame = random.choice(OBSTACLES_FRAMES)
        frame_height, frame_width = get_frame_size(frame)
        column = random.randint(1, canvas_width - frame_width - 1)
        obstacle = Obstacle(0, column, frame_height, frame_width, uid=uuid.uuid4())
        obstacles.append(obstacle)
        coroutines.append(fly_garbage(canvas, obstacle, frame, rand(.05, .1)))
        logging.debug("Obstacles count: %d", len(obstacles))


def draw(canvas):
    """create anumations coroutines and run event loop"""
    coroutines.extend([
        blink(canvas, row, column, random.choice(STARS), random.randint(0, 1))
        for row, column in get_random_coordinates_list(canvas)
    ])
    ship = Ship.factory(*get_canvas_center(canvas))
    coroutines.append(ship.animate())
    coroutines.append(handle_inputs(canvas, ship))
    coroutines.append(ship.check_collision(canvas))
    coroutines.append(fill_orbit_with_garbage(canvas))
    loop.run(canvas, coroutines)


def main():
    """prepare canvas and use the draw function"""
    logging.basicConfig(
        filename=os.path.join(BASE_DIR, '../spaceship.log'), level=LOG_LEVEL
    )

    try:
        screen = curses.initscr()
        curses.start_color()
        screen.border()
        screen.nodelay(True)
        curses.update_lines_cols()
        curses.curs_set(False)
        curses.wrapper(draw)
    except KeyboardInterrupt:
        curses.endwin()
        print("Good Bye, major Tom")


if __name__ == "__main__":
    main()
