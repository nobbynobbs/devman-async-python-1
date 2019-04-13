"""gameover banner"""

import os

from core.constants import BASE_DIR
from curses_tools import get_frame_size, draw_frame


with open(os.path.join(BASE_DIR, "frames", "gameover.txt")) as f_d:
    GAMEOVER_FRAME = f_d.read()


class GameOver:
    """game over banner"""
    def __init__(self, canvas):
        size_rows, size_columns = get_frame_size(GAMEOVER_FRAME)
        canvas_rows, canvas_columns = canvas.getmaxyx()
        self.canvas = canvas
        self.row = (canvas_rows - size_rows) // 2
        self.column = (canvas_columns - size_columns) // 2

    def show(self):
        """draw gameover banner on the canvas"""
        draw_frame(self.canvas, self.row, self.column, GAMEOVER_FRAME)

    def hide(self):
        """erase gamover banner from canvas"""
        draw_frame(self.canvas, self.row, self.column, GAMEOVER_FRAME, negative=True)
