#!/usr/bin/env python3

"""application entry point"""

import asyncio
import curses
import logging
import os

from core.constants import BASE_DIR
import core.loop as loop
from curses_tools import get_canvas_center, read_controls
from settings import LOG_LEVEL
from state import coroutines, obstacles
from objects.gameover import GameOver
from objects.ship import Ship
from objects.stars import get_stars_coroutines
from objects.obstacles import fill_space_with_obstacles


def draw(canvas):
    """create animations coroutines and run event loop"""
    coroutines.extend(get_stars_coroutines(canvas))
    ship = Ship.factory(*get_canvas_center(canvas))
    ship.start(canvas)
    coroutines.append(handle_inputs(canvas, ship))
    coroutines.append(fill_space_with_obstacles(canvas))
    loop.run(canvas, coroutines)


async def handle_inputs(canvas, ship):
    """async wrapper for controls handler"""
    gameover = GameOver(canvas)
    while True:
        row, column, shoot = read_controls(canvas)  # non-blocking
        if not ship.destroyed:
            gameover.hide()
            await ship.move(canvas, row, column)
            if shoot:
                ship.shoot(canvas)
        else:
            gameover.show()
            if shoot:
                for obstacle in obstacles:
                    obstacle.destroyed = True
                    ship.destroyed = False
                    ship.start(canvas)
            await asyncio.sleep(0)


def main():
    """prepare canvas and use the draw function"""
    logging.basicConfig(
        filename=os.path.join(BASE_DIR, "../spaceship.log"), level=LOG_LEVEL
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
