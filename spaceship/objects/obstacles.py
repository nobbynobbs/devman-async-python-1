"""obstacle class, animations and factory"""

import asyncio
import logging
import random
import uuid

from core.animations import explode
from core import loop
from core.constants import OBSTACLES_FRAMES
from curses_tools import draw_frame, get_frame_size
from settings import DEBUG, MIN_OBSTACLES_SPEED, MAX_OBSTACLES_SPEED
from state import obstacles, coroutines
from utils import rand

class Obstacle:
    """cosmic garbage"""
    def __init__(self, row, column, rows_size=1, columns_size=1, uid=None):
        self.row = row
        self.column = column
        self.rows_size = rows_size
        self.columns_size = columns_size
        self.uid = uid
        self.destroyed = False

    @property
    def center(self):
        """coordinates of center"""
        return self.row + self.rows_size // 2, self.column + self.columns_size // 2

    def get_bounding_box_frame(self):
        """increment box size to compensate obstacle movement"""
        rows, columns = self.rows_size + 1, self.columns_size + 1
        return "\n".join(_get_bounding_box_lines(rows, columns))

    def get_bounding_box_corner_pos(self):
        return self.row - 1, self.column - 1

    def dump_bounding_box(self):
        row, column = self.get_bounding_box_corner_pos()
        return row, column, self.get_bounding_box_frame()

    def has_collision(
        self, obj_corner_row, obj_corner_column, obj_size_rows=1, obj_size_columns=1
    ):
        """Determine if collision has occured. Return True or False."""
        return has_collision(
            (self.row, self.column),
            (self.rows_size, self.columns_size),
            (obj_corner_row, obj_corner_column),
            (obj_size_rows, obj_size_columns),
        )

    async def fly(self, canvas, garbage_frame, speed=0.5):
        """Animate garbage, flying from top to bottom.
        Сolumn position will stay same, as specified on start."""
        rows_number, columns_number = canvas.getmaxyx()

        column = max(self.column, 0)
        column = min(column, columns_number - 1)

        while self.row < rows_number:
            draw_frame(canvas, self.row, column, garbage_frame)
            await asyncio.sleep(0)
            draw_frame(canvas, self.row, column, garbage_frame, negative=True)
            if self.destroyed:
                obstacles.remove(self)
                await explode(canvas, *self.center)
                return
            self.row += speed
        obstacles.remove(self)


def _get_bounding_box_lines(rows, columns):
    """yield bounding box line by line"""
    yield " " + "-" * columns + " "
    for _ in range(rows):
        yield "|" + " " * columns + "|"
    yield " " + "-" * columns + " "


async def show_obstacles(canvas):
    """Display bounding boxes of every obstacle in a list"""

    while True:
        boxes = []

        for obstacle in obstacles:
            boxes.append(obstacle.dump_bounding_box())

        for row, column, frame in boxes:
            draw_frame(canvas, row, column, frame)

        await asyncio.sleep(0)

        for row, column, frame in boxes:
            draw_frame(canvas, row, column, frame, negative=True)


def _is_point_inside(
    corner_row, corner_column, size_rows, size_columns, point_row, point_row_column
):
    rows_flag = corner_row <= point_row < corner_row + size_rows
    columns_flag = corner_column <= point_row_column < corner_column + size_columns

    return rows_flag and columns_flag


def has_collision(obstacle_corner, obstacle_size, obj_corner, obj_size=(1, 1)):
    """Determine if collision has occured. Return True or False."""

    opposite_obstacle_corner = (
        obstacle_corner[0] + obstacle_size[0] - 1,
        obstacle_corner[1] + obstacle_size[1] - 1,
    )

    opposite_obj_corner = (
        obj_corner[0] + obj_size[0] - 1,
        obj_corner[1] + obj_size[1] - 1,
    )

    return any(
        [
            _is_point_inside(*obstacle_corner, *obstacle_size, *obj_corner),
            _is_point_inside(*obstacle_corner, *obstacle_size, *opposite_obj_corner),
            _is_point_inside(*obj_corner, *obj_size, *obstacle_corner),
            _is_point_inside(*obj_corner, *obj_size, *opposite_obstacle_corner),
        ]
    )


async def fill_space_with_obstacles(canvas):
    """generates infinite obstacles flow"""
    _, canvas_width = canvas.getmaxyx()
    if DEBUG:
        coroutines.append(show_obstacles(canvas))
    while True:
        await loop.sleep(random.random() * 2)  # sleep [0, 2] seconds
        frame = random.choice(OBSTACLES_FRAMES)
        frame_height, frame_width = get_frame_size(frame)
        column = random.randint(1, canvas_width - frame_width - 1)
        obstacle = Obstacle(0, column, frame_height, frame_width, uid=uuid.uuid4())
        obstacles.append(obstacle)
        coroutines.append(obstacle.fly(canvas, frame, _get_random_speed()))
        logging.debug("Obstacles count: %d", len(obstacles))


def _get_random_speed():
    """return random speed for obstacle"""
    return rand(MIN_OBSTACLES_SPEED, MAX_OBSTACLES_SPEED)
