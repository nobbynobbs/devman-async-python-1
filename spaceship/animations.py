"""async animation functions"""

import asyncio
import curses
import os

from constants import BASE_DIR
from curses_tools import draw_frame, get_frame_size
from state import obstacles
from utils import sleep, read_frames

EXPLOSION_FRAMES = read_frames(os.path.join(BASE_DIR, "frames", "explosion"))


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot. Direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), "*")
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), "O")
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), " ")

    row += rows_speed
    column += columns_speed

    symbol = "-" if columns_speed else "|"

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), " ")
        for obstacle in obstacles:
            if obstacle.has_collision(row, column):
                obstacle.destroyed = True
                return
        row += rows_speed
        column += columns_speed


async def blink(canvas, row, column, symbol="*", delay=0):
    """display twinkle twinkle little star"""
    await sleep(delay)
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(2)

        canvas.addstr(row, column, symbol)
        await sleep(0.3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(0.5)

        canvas.addstr(row, column, symbol)
        await sleep(0.3)


async def fly_garbage(canvas, obstacle, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom.
    Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(obstacle.column, 0)
    column = min(column, columns_number - 1)

    while obstacle.row < rows_number:
        draw_frame(canvas, obstacle.row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, obstacle.row, column, garbage_frame, negative=True)
        if obstacle.destroyed:
            obstacles.remove(obstacle)
            await explode(canvas, *obstacle.center)
            return
        obstacle.row += speed
    obstacles.remove(obstacle)


async def explode(canvas, center_row, center_column):
    rows, columns = get_frame_size(EXPLOSION_FRAMES[0])
    corner_row = center_row - rows / 2
    corner_column = center_column - columns / 2

    curses.beep()
    for frame in EXPLOSION_FRAMES:

        draw_frame(canvas, corner_row, corner_column, frame)

        await asyncio.sleep(0)
        draw_frame(canvas, corner_row, corner_column, frame, negative=True)
        await asyncio.sleep(0)
