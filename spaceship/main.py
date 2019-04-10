#!/usr/bin/env python3

"""event loop and entry point"""

import curses
import itertools
import os
import time
import random

from curses_tools import draw_frame, get_frame_size

from animations import blink, fire, fly_garbage
from constants import SPACESHIP_FRAMES_DIR, TIC_TIMEOUT, STARS, BASE_DIR
from utils import (
    sleep,
    read_frames,
    get_random_coordinates_list,
    get_canvas_center,
    handle_inputs,
)


class Position:
    """point on screen"""

    def __init__(self, row, column):
        self.row = row
        self.column = column

    def move(self, row_direction, column_direction):
        """shift position"""
        self.row += row_direction
        self.column += column_direction

    def position(self):
        "return current row and column"
        return self.row, self.column


class Ship:
    """Define spaceship properties and behaviour"""

    ALLOWED_DIRECTIONS = {-1, 0, 1}

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
        """change ship position"""
        if not all(
            [
                self._direction_value_is_alowed(row_direction),
                self._direction_value_is_alowed(column_direction),
            ]
        ):
            raise ValueError(
                "Both direction values must be from set {}, ({}, {}) passed".format(
                    self.ALLOWED_DIRECTIONS, row_direction, column_direction
                )
            )

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

    @classmethod
    def _direction_value_is_alowed(cls, direction):
        """check if direction value is allowed"""
        return direction in cls.ALLOWED_DIRECTIONS

    @property
    def size(self):
        """return size of rendered frame"""
        if self.current_frame is None:
            return 0, 0
        return get_frame_size(self.current_frame)

    def can_move(self, canvas, row_direction, column_direction):
        """check if ship reached the canvas border"""
        border_width = 1
        frame_height, frame_width = self.size
        canvas_height, canvas_width = canvas.getmaxyx()
        return not any(
            [
                self.position.column <= border_width and column_direction < 0,
                self.position.row <= border_width and row_direction < 0,
                self.position.row + frame_height >= canvas_height - border_width
                and row_direction > 0,
                self.position.column + frame_width >= canvas_width - border_width
                and column_direction > 0,
            ]
        )

    @classmethod
    def factory(cls, row, col):
        """create new ship instance"""
        frames = read_frames(SPACESHIP_FRAMES_DIR)
        return Ship(Position(row, col), frames)


async def fill_orbit_with_garbage(coroutines, canvas):
    """generates infinite garbage frames"""
    frames = read_frames(os.path.join(BASE_DIR, 'frames/garbage'))
    _, canvas_width = canvas.getmaxyx()
    while True:
        await sleep(random.random() * 2)  # sleep [0, 2] seconds
        frame = random.choice(frames)
        frame_width, _ = get_frame_size(frame)
        column = random.randint(1, canvas_width - frame_width - 2)
        coroutines.append(fly_garbage(canvas, column, frame, .2))


def draw(canvas):
    """create anumations coroutines and run event loop"""
    coroutines = [
        blink(canvas, row, column, random.choice(STARS), random.randint(0, 1))
        for row, column in get_random_coordinates_list(canvas)
    ]
    fire_coro = fire(canvas, *get_canvas_center(canvas))
    coroutines.append(fire_coro)
    ship = Ship.factory(*get_canvas_center(canvas))
    coroutines.append(ship.render(canvas))
    coroutines.append(handle_inputs(ship, canvas))
    coroutines.append(fill_orbit_with_garbage(coroutines, canvas))
    run_loop(coroutines, canvas)


def run_loop(coroutines, canvas):
    """invoke coroutines, collect exhausted coroutines"""
    while coroutines:
        # is it ok to allocate new set on each iteration?
        finished_coroutines = set()
        for coro in coroutines:
            try:
                coro.send(None)
            except StopIteration:
                finished_coroutines.add(coro)
        canvas.refresh()
        for coro in finished_coroutines:
            coroutines.remove(coro)
        time.sleep(TIC_TIMEOUT)  # limit event-loop frequency
        canvas.border()


def main():
    """prepare canvas and use the draw function"""
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
