"""base class for frame-based objects"""

from curses_tools import get_frame_size, draw_frame


class Frame:
    """frame wrapper"""
    def __init__(self, canvas, frame, row, column):
        self.canvas = canvas
        self.frame = frame
        self.row = row
        self.column = column
        self.rows_size, self.columns_size = get_frame_size(frame)

    @property
    def size(self):
        """return tuple size_rows, size_columns"""
        return self.rows_size, self.columns_size

    @property
    def center(self):
        """coordinates of center"""
        return self.row + self.rows_size // 2, self.column + self.columns_size // 2

    def show(self):
        """show frame on canvas"""
        draw_frame(self.canvas, self.row, self.column, self.frame)

    def hide(self):
        """hide frame from canvas"""
        draw_frame(self.canvas, self.row, self.column, self.frame, negative=True)
