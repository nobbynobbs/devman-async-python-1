#!/usr/bin/env python3

"""application entry point"""

import asyncio
import curses
import logging
import os

from core.constants import BASE_DIR, GAMEOVER_FRAME
import core.loop as loop
from curses_tools import get_canvas_center, read_controls, get_justify_offset
from settings import LOG_LEVEL, SPACE_ERA_BEGINNING
from state import coroutines, obstacles
from objects.frame import Frame
from objects.ship import new_ship
from objects.stars import get_stars_coroutines
from objects.obstacles import fill_space_with_obstacles
from objects.timeline import Timeline, show as show_timeline


def draw(canvas):
    """create animations coroutines and run event loop"""
    coroutines.extend(get_stars_coroutines(canvas))
    timeline = Timeline(year=SPACE_ERA_BEGINNING)
    coroutines.extend([timeline.run(), show_timeline(canvas, timeline)])
    ship = new_ship(canvas, *get_canvas_center(canvas))
    ship.start()
    coroutines.append(handle_inputs(canvas, ship))
    coroutines.append(fill_space_with_obstacles(canvas, timeline))
    loop.run(canvas, coroutines)


async def handle_inputs(canvas, ship):
    """async wrapper for controls handler"""
    gameover = Frame(
        canvas, GAMEOVER_FRAME, *get_justify_offset(canvas, GAMEOVER_FRAME)
    )
    while True:
        row, column, shoot = read_controls(canvas)  # non-blocking
        if not ship.destroyed:
            gameover.hide()
            await ship.move(row, column)
            if shoot:
                ship.shoot()
        else:
            gameover.show()
            if shoot:
                for obstacle in obstacles:
                    obstacle.destroyed = True
                    await asyncio.sleep(0)
                    exit(0)
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
