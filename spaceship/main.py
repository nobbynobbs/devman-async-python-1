#!/usr/bin/env python3

"""application entry point"""

import asyncio
import curses
import logging
import os

from core.animations import Explosion
from core.constants import BASE_DIR
import core.loop as loop
from curses_tools import get_canvas_center, read_controls, get_justify_offset
from settings import LOG_LEVEL, SPACE_ERA_BEGINNING
from state import coroutines, obstacles
from objects.frame import Frame
from objects.ship import new_ship
from objects.stars import get_stars_coroutines
from objects.obstacles import fill_space_with_garbage
from objects.timeline import Timeline, show as show_timeline
from utils import read_all_frames


def create_coroutines(canvas):
    """create coroutines for execution"""
    try:
        frames = read_all_frames()
    except IOError:
        logging.critical("could not read frames")
        exit(1)

    explosion = Explosion(canvas, frames["explosion"])
    coroutines.extend(get_stars_coroutines(canvas))
    timeline = Timeline(year=SPACE_ERA_BEGINNING)
    coroutines.extend([timeline.run(), show_timeline(canvas, timeline)])
    ship = new_ship(canvas, *get_canvas_center(canvas), frames["spaceship"], explosion)
    ship.start()
    coroutines.append(handle_inputs(canvas, ship, frames))
    coroutines.append(
        fill_space_with_garbage(canvas, timeline, frames["garbage"], explosion)
    )


def draw(canvas):
    """create animations coroutines and run event loop"""
    create_coroutines(canvas)
    loop.run(canvas, coroutines)


async def handle_inputs(canvas, ship, frames):
    """async wrapper for controls handler"""
    gameover = Frame(
        canvas, frames["gameover"], *get_justify_offset(canvas, frames["gameover"])
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


def init_curses():
    """initialize curses"""
    screen = curses.initscr()
    curses.start_color()
    screen.border()
    screen.nodelay(True)
    curses.update_lines_cols()
    curses.curs_set(False)


def main():
    """prepare canvas and use the draw function"""
    logging.basicConfig(
        filename=os.path.join(BASE_DIR, "../spaceship.log"), level=LOG_LEVEL
    )
    init_curses()
    try:
        curses.wrapper(draw)
    except KeyboardInterrupt:
        curses.endwin()
        print("Good Bye, major Tom")


if __name__ == "__main__":
    main()
