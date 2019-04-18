"""common (reusable) async animation functions"""

import asyncio
import curses

from objects import frame as mframe
from state import obstacles


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


class Explosion:
    """wrapper for explosion animation"""
    __slots__ = ("canvas", "frames")

    def __init__(self, canvas, frames):
        self.canvas = canvas
        self.frames = [mframe.Frame(canvas, frame, None, None) for frame in frames]

    async def explode(self, center_row, center_column):
        """exlplosion animation"""
        rows, columns = self.frames[0].size
        corner_row = center_row - rows / 2
        corner_column = center_column - columns / 2
        curses.beep()
        for frame in self.frames:
            frame.show(corner_row, corner_column)
            await asyncio.sleep(0)
            frame.hide(corner_row, corner_column)
            await asyncio.sleep(0)
