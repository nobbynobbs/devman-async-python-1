import asyncio


class Garbage:
    def __init__(self, canvas, row, column, frame, explosion):
        self.canvas = canvas
        self.row = row
        self.column = column
        self.frame = frame
        self.explosion = explosion
        self.destroyed = False

    @property
    def center(self):
        return (
            self.row + self.frame.rows_size // 2,
            self.column + self.frame.columns_size // 2,
        )

    @property
    def size(self):
        return self.frame.size

    @property
    def rows_size(self):
        return self.frame.rows_size

    @property
    def columns_size(self):
        return self.frame.columns_size

    async def render_frame(self):
        self.frame.show(self.row, self.column)
        await asyncio.sleep(0)
        self.frame.hide(self.row, self.column)

    async def fly(self, speed=0.5):
        """Animate garbage, flying from top to bottom.
        Сolumn position will stay same, as specified on start."""
        rows_number, columns_number = self.canvas.getmaxyx()

        column = max(self.column, 0)
        column = min(column, columns_number - 1)

        while self.row < rows_number:
            await self.render_frame()
            if self.destroyed:
                await self.explosion.explode(*self.center)
                return
            self.row += speed
        self.destroyed = True  # fly out of screen
