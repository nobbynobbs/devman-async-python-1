#!/usr/bin/env python3

import asyncio
import curses
import itertools
import os
import time
import random

from curses_tools import draw_frame, read_controls, get_frame_size

from animations import blink
from constants import BASE_DIR, TIC_TIMEOUT, STARS
from utils import sleep, read_frames, random_coordinates_list, canvas_center

class Position:
    """point on screen"""
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def move(self, row_direction, column_direction):
        self.row += row_direction
        self.column += column_direction


class Ship:
    """Spaceship"""
    def __init__(self, position, frames):
        self.position = position
        self.frames = frames
        self.current_frame = None

    async def render(self, canvas):
        """async render"""
        for frame in itertools.cycle(self.frames):
            self.current_frame = frame
            draw_frame(canvas, self.position.row, self.position.column, frame)
            await sleep(0.1)
            draw_frame(
                canvas, self.position.row, self.position.column, frame, negative=True
            )

    def move(self, row_direction, column_direction, canvas):
        if row_direction == 0 and column_direction == 0:
            return
        if self.can_move(canvas, row_direction, column_direction):
            draw_frame(
                canvas,
                self.position.row,
                self.position.column,
                self.current_frame,
                negative=True,
            )
            self.position.move(row_direction, column_direction)
            draw_frame(
                canvas, self.position.row, self.position.column, self.current_frame
            )

    @property
    def size(self):
        if self.current_frame is None:
            return 0, 0
        return get_frame_size(self.current_frame)

    def can_move(self, canvas, row_direction, column_direction):
        height, width = self.size
        canvas_height, canvas_width = canvas.getmaxyx()
        if self.position.column < width // 2 and column_direction < 0:
            return False
        if self.position.row < height // 4 and row_direction < 0:
            return False
        if self.position.row + height > canvas_height - 2 and row_direction > 0:
            return False
        if self.position.column + width > canvas_width - 2 and column_direction > 0:
            return False
        return True

    @classmethod
    def factory(cls, row, col):
        frames = read_frames()
        return Ship(Position(row, col), frames)


def draw(canvas):
    
    coroutines = [
        blink(canvas, row, column, random.choice(STARS))
        for row, column in random_coordinates_list(canvas)
    ]
    
    ship = Ship.factory(*canvas_center(canvas))
    coroutines.append(ship.render(canvas))

    finished_coroutines = set()
    while len(coroutines):
        for coro in coroutines:
            try:
                coro.send(None)
                row, column, _ = read_controls(canvas)  # non-blocking
                ship.move(row, column, canvas)
            except StopIteration:
                finished_coroutines.add(coro)
        canvas.refresh()
        for coro in finished_coroutines:    
            coroutines.remove(coro)
        finished_coroutines.clear()
        time.sleep(TIC_TIMEOUT)  # limit event-loop frequency


def main():
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
