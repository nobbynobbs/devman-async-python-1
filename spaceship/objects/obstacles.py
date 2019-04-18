"""obstacle class, animations and factory"""

import asyncio
import logging
import random

from core import loop
from curses_tools import draw_frame
from objects import garbage, frame as mframe
from settings import (
    MIN_OBSTACLES_SPEED,
    MAX_OBSTACLES_SPEED,
    SPACE_ERA_BEGINNING,
    YEAR_IN_SECONDS,
)
from state import obstacles, coroutines
from utils import rand


class Obstacle():
    """cosmic garbage"""

    def __init__(self, obstacle):
        self.obstacle = obstacle

    @property
    def destroyed(self):
        return self.obstacle.destroyed

    @destroyed.setter
    def destroyed(self, value):
        self.obstacle.destroyed = value

    @property
    def rows_size(self):
        return self.obstacle.rows_size

    @property
    def columns_size(self):
        return self.obstacle.columns_size

    @property
    def row(self):
        return self.obstacle.row

    @property
    def column(self):
        return self.obstacle.column

    def get_bounding_box_frame(self):
        """increment box size to compensate obstacle movement"""
        rows, columns = self.rows_size + 1, self.columns_size + 1
        return "\n".join(_get_bounding_box_lines(rows, columns))

    def get_bounding_box_corner_pos(self):
        """top left corner"""
        return self.row - 1, self.column - 1

    def dump_bounding_box(self):
        """left top corner and bbox frame itself"""
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
        dead_obstacles = [obstacle for obstacle in obstacles if obstacle.destroyed]
        for obstacle in dead_obstacles:
            obstacles.remove(obstacle)

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


async def fill_space_with_garbage(canvas, timeline, frames, explosion):
    """generates infinite garbage flow"""
    _, canvas_width = canvas.getmaxyx()
    while True:
        try:
            sleeping_time = YEAR_IN_SECONDS / (timeline.year - SPACE_ERA_BEGINNING)
        except ZeroDivisionError:
            sleeping_time = YEAR_IN_SECONDS

        await loop.sleep(sleeping_time)
        raw_frame = random.choice(frames)
        frame = mframe.Frame(canvas, raw_frame, None, None)
        column = random.randint(1, canvas_width - frame.columns_size - 1)
        garbage_instance = garbage.Garbage(canvas, 0, column, frame, explosion)
        obstacle = Obstacle(garbage_instance)
        obstacles.append(obstacle)
        coroutines.append(garbage_instance.fly(_get_random_speed()))
        logging.debug("Obstacles count: %d", len(obstacles))


def _get_random_speed():
    """return random speed for obstacle"""
    return rand(MIN_OBSTACLES_SPEED, MAX_OBSTACLES_SPEED)
