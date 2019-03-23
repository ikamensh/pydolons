from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List, Union, Callable
    from game_objects.battlefield_objects import BattlefieldObject, Unit, Obstacle
    from battlefield import Cell

class Dungeon:
    def __init__(self, name: str, h: int, w: int, *,
                 objs: Callable[[], List[BattlefieldObject]],
                 hero_entrance: Union[Cell, complex],
                 icon="dungeon.png"):

        self.name = name

        self.objs = objs
        self.h = h
        self.w = w
        self.hero_entrance = hero_entrance

        self.icon = icon

    @property
    def tooltip_info(self):
        return self.name

