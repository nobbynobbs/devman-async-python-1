"""simple year container"""

import dataclasses

from core.loop import sleep
from settings import YEAR_IN_SECONDS


@dataclasses.dataclass
class Timeline:
    """use mutable object intead global variable"""

    year: int

    async def run(self):
        """periodically increments the year"""
        while True:
            await sleep(YEAR_IN_SECONDS)
            self.year += 1


async def show(canvas, timeline):
    """draw the year on canvas"""
    while True:
        canvas.addstr(2, 3, "{}".format(timeline.year))
        await sleep(0.2)
