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
        """return tuple rows_size, columns_size"""
        return self.rows_size, self.columns_size

    @property
    def center(self):
        """coordinates of center"""
        return self.row + self.rows_size // 2, self.column + self.columns_size // 2

    def show(self, row=None, column=None):
        """show frame on canvas
        we can override row and column attributes
        """
        row, column = self._override_row_and_column(row, column)
        draw_frame(self.canvas, row, column, self.frame)

    def hide(self, row=None, column=None):
        """hide frame from canvas
        we can override row and column attributes
        """
        row, column = self._override_row_and_column(row, column)
        draw_frame(self.canvas, row, column, self.frame, negative=True)

    def _override_attribute_value(self, attribute, value):
        """"""
        if value is None:
            return getattr(self, attribute)
        return value

    def _override_row_and_column(self, row, column):
        row = self._override_attribute_value("row", row)
        column = self._override_attribute_value("column", column)
        return row, column
