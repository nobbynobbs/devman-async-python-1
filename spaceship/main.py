#!/usr/bin/env python3

"""event loop and entry point"""

import curses
import logging
import os

import core.loop as loop
from core.constants import BASE_DIR
from curses_tools import get_canvas_center
from settings import LOG_LEVEL
from state import coroutines
from objects.stars import get_stars_coroutines
from objects.obstacles import fill_space_with_obstacles
from objects.ship import Ship
from utils import handle_inputs


def draw(canvas):
    """create anumations coroutines and run event loop"""
    coroutines.extend(get_stars_coroutines(canvas))
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
