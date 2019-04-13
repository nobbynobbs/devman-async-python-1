#!/usr/bin/env python3

"""event loop and entry point"""

import curses
import logging
import os
import random

from animations import blink
import core.loop as loop
from core.constants import STARS, BASE_DIR
from settings import LOG_LEVEL
from state import coroutines
from obstacles import fill_space_with_obstacles
from ship import Ship
from utils import (
    get_random_coordinates_list,
    get_canvas_center,
    handle_inputs,
)


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
    coroutines.append(fill_space_with_obstacles(canvas))
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
