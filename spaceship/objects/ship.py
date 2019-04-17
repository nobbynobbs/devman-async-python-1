"""spaceship related classes"""

import itertools
import logging

from core.animations import fire
from core.loop import sleep
from core.physics import update_speed
from objects.frame import Frame
from state import coroutines, obstacles


class Ship:
    """Define spaceship properties and behaviour"""

    def __init__(self, canvas, row, column, frames, explosion):
        self.canvas = canvas
        self.row = row
        self.column = column
        self.explosion = explosion
        self.row_speed = 0
        self.column_speed = 0
        self.current_frame = None
        self.previous_frame = None
        self.destroyed = False
        self.frames = itertools.cycle([Frame(canvas, frame, 0, 0) for frame in frames])

    def start(self):
        """add infinite ship's coroutines into event loop"""
        coroutines.extend([self.animate(), self.check_collision()])

    @property
    def size(self):
        """return size of rendered frame"""
        if self.current_frame is None:
            return 0, 0
        return self.current_frame.size

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

    async def move(self, row_direction, column_direction):
        """change ship position"""

        border_width = 0
        frame_height, frame_width = self.size
        canvas_height, canvas_width = self.canvas.getmaxyx()

        negative_frame = self.previous_frame or self.current_frame
        negative_frame.hide(self.row, self.column)

        self.update_speed(row_direction, column_direction)
        logging.debug(
            "row speed: %.3f, column speed: %.3f", self.row_speed, self.column_speed
        )
        if (
            self.column - self.column_speed <= border_width + 1
            and column_direction <= 0
        ):
            self.column = border_width + 1
            self.column_speed = 0

        if (
            self.column + frame_width + self.column_speed >= canvas_width - border_width
            and column_direction >= 0
        ):
            self.column = canvas_width - frame_width - border_width - 1
            self.column_speed = 0

        if self.row - self.row_speed <= border_width and row_direction <= 0:
            self.row = border_width + 1
            self.row_speed = 0

        if (
            self.row + frame_height + self.row_speed >= canvas_height - border_width
            and row_direction >= 0
        ):
            self.row = canvas_height - border_width - 1 - frame_height
            self.row_speed = 0

        self.column += self.column_speed
        self.row += self.row_speed

        self.current_frame.show(self.row, self.column)
        self.previous_frame = self.current_frame
        await sleep(0)

    async def explode(self):
        """animete ship destroying"""
        negative_frame = self.previous_frame or self.current_frame
        negative_frame.hide(self.row, self.column)
        height, width = self.size
        await self.explosion.explode(
            self.row + height // 2, self.column + width // 2
        )

    def shoot(self):
        """create lasergun shot"""
        coroutines.append(
            fire(
                self.canvas,
                self.row,
                self.column + self.current_frame.columns_size // 2,
            )
        )

    async def check_collision(self):
        """mark ship as destroyed if there is collision with obstacles"""
        while True:
            for obstacle in obstacles:
                if obstacle.has_collision(self.row, self.column, *self.size):
                    logging.debug("Ship must be destroyed")
                    self.destroyed = True
                    await self.explode()
                    return
            await sleep(0)


def new_ship(canvas, row, column, frames, explosion):
    """create new ship instance"""
    return Ship(canvas, row, column, frames, explosion)
