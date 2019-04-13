#!/usr/bin/env python3

"""event loop and entry point"""

import dataclasses
import curses
import itertools
import os
import time
import random
import uuid

from animations import blink, fire, fly_garbage
from constants import SPACESHIP_FRAMES_DIR, TIC_TIMEOUT, STARS, BASE_DIR
from curses_tools import draw_frame, get_frame_size
from state import coroutines, obstacles
from obstacles import Obstacle, show_obstacles
from physics import update_speed
from utils import (
    sleep,
    read_frames,
    get_random_coordinates_list,
    get_canvas_center,
    handle_inputs,
)


@dataclasses.dataclass
class Position:
    """point on screen"""

    row: float
    column: float

    def move(self, row_direction, column_direction):
        """shift position"""
        self.row += row_direction
        self.column += column_direction

    def position(self):
        "return current row and column"
        return self.row, self.column


class Ship:
    """Define spaceship properties and behaviour"""

    def __init__(self, position, frames, row_speed=0, column_speed=0):
        self.position = position
        self.row_speed = row_speed
        self.column_speed = column_speed
        self.frames = itertools.cycle(frames)
        self.current_frame = None
        self.previous_frame = None

    def update_speed(self, row_direction, column_direction):
        self.row_speed, self.column_speed = update_speed(
            self.row_speed, self.column_speed, row_direction, column_direction
        )

    async def animate(self):
        for frame in self.frames:
            self.current_frame = frame
            await sleep(0.1)

    async def move(self, canvas, row_direction, column_direction):
        """change ship position"""

        border_width = 0
        frame_height, frame_width = self.size
        canvas_height, canvas_width = canvas.getmaxyx()

        negative_frame = self.previous_frame or self.current_frame

        draw_frame(
            canvas,
            self.position.row,
            self.position.column,
            negative_frame,
            negative=True,
        )
        self.update_speed(row_direction, column_direction)

        if (
            self.position.column - self.column_speed <= border_width + 1
            and column_direction <= 0
        ):
            self.position.column = border_width + 1
            self.column_speed = 0

        if (
            self.position.column + frame_width + self.column_speed
            >= canvas_width - border_width
            and column_direction >= 0
        ):
            self.position.column = canvas_width - frame_width - border_width - 1
            self.column_speed = 0

        if self.position.row - self.row_speed <= border_width and row_direction <= 0:
            self.position.row = border_width + 1
            self.row_speed = 0

        if (
            self.position.row + frame_height + self.row_speed
            >= canvas_height - border_width
            and row_direction >= 0
        ):
            self.position.row = canvas_height - border_width - 1 - frame_height
            self.row_speed = 0

        self.position.column += self.column_speed
        self.position.row += self.row_speed

        draw_frame(canvas, self.position.row, self.position.column, self.current_frame)
        self.previous_frame = self.current_frame
        await sleep(0)

    def shoot(self, canvas):
        _, ship_width = self.size
        coroutines.append(
            fire(canvas, self.position.row, self.position.column + ship_width // 2)
        )

    @property
    def size(self):
        """return size of rendered frame"""
        if self.current_frame is None:
            return 0, 0
        return get_frame_size(self.current_frame)

    @classmethod
    def factory(cls, row, col):
        """create new ship instance"""
        frames = read_frames(SPACESHIP_FRAMES_DIR)
        return Ship(Position(row, col), frames)


async def fill_orbit_with_garbage(canvas):
    """generates infinite garbage frames"""
    frames = read_frames(os.path.join(BASE_DIR, "frames/garbage"))
    _, canvas_width = canvas.getmaxyx()
    while True:
        await sleep(random.random() * 2)  # sleep [0, 2] seconds
        frame = random.choice(frames)
        frame_height, frame_width = get_frame_size(frame)
        column = random.randint(1, canvas_width - frame_width - 1)
        obstacle = Obstacle(0, column, frame_height, frame_width, uid=uuid.uuid4())
        obstacles.append(obstacle)
        coroutines.append(fly_garbage(canvas, obstacle, frame, 0.2))
        coroutines.append(show_obstacles(canvas, obstacles))


def draw(canvas):
    """create anumations coroutines and run event loop"""
    global coroutines
    coroutines += [
        blink(canvas, row, column, random.choice(STARS), random.randint(0, 1))
        for row, column in get_random_coordinates_list(canvas)
    ]
    ship = Ship.factory(*get_canvas_center(canvas))
    coroutines.append(ship.animate())
    coroutines.append(handle_inputs(ship, canvas))
    coroutines.append(fill_orbit_with_garbage(canvas))
    run_loop(canvas)


def run_loop(canvas):
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
