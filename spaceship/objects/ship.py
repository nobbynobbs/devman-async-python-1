"""spaceship related classes"""

import dataclasses
import itertools
import logging

from core.animations import explode as animate_explosion, fire
from core.constants import SPACESHIP_FRAMES
from core.loop import sleep
from core.physics import update_speed
from curses_tools import get_frame_size, draw_frame
from state import coroutines, obstacles


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
        self.destroyed = False

    @property
    def row(self):
        """row getter"""
        return self.position.row

    @property
    def column(self):
        """column getter"""
        return self.position.column

    @property
    def size(self):
        """return size of rendered frame"""
        if self.current_frame is None:
            return 0, 0
        return get_frame_size(self.current_frame)

    def update_speed(self, row_direction, column_direction):
        """update ship speed"""
        self.row_speed, self.column_speed = update_speed(
            self.row_speed, self.column_speed, row_direction, column_direction
        )

    async def animate(self):
        """toggle frames"""
        for frame in self.frames:
            self.current_frame = frame
            await sleep(0.1)

    async def move(self, canvas, row_direction, column_direction):
        """change ship position"""

        border_width = 0
        frame_height, frame_width = self.size
        canvas_height, canvas_width = canvas.getmaxyx()

        negative_frame = self.previous_frame or self.current_frame

        draw_frame(canvas, self.row, self.column, negative_frame, negative=True)
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

    async def explode(self, canvas):
        """animete ship destroying"""
        negative_frame = self.previous_frame or self.current_frame
        height, width = self.size
        draw_frame(canvas, self.row, self.column, negative_frame, negative=True)
        await animate_explosion(
            canvas, self.row + height // 2, self.column + width // 2
        )

    def shoot(self, canvas):
        """create lasergun shot"""
        _, ship_width = self.size
        coroutines.append(
            fire(canvas, self.position.row, self.position.column + ship_width // 2)
        )

    @classmethod
    def factory(cls, row, col):
        """create new ship instance"""
        return Ship(Position(row, col), SPACESHIP_FRAMES)

    async def check_collision(self, canvas):
        """mark ship as destroyed if there is collision with obstacles"""
        while True:
            for obstacle in obstacles:
                if obstacle.has_collision(self.row, self.column, *self.size):
                    logging.debug("Ship must be destroyed")
                    self.destroyed = True
                    await self.explode(canvas)
                    return
            await sleep(0)
