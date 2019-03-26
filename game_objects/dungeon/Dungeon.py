from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List, Union, Callable, Collection
    from game_objects.battlefield_objects import BattlefieldObject, Wall
    from battlefield import Cell
    from DreamGame import DreamGame

class Dungeon:
    @property
    def tooltip_info(self):
        return self.name
    def __init__(self, name: str, h: int, w: int, *,
                 construct_objs: Callable[[DreamGame], Collection[BattlefieldObject]],
                 hero_entrance: Union[Cell, complex],
                 construct_walls: Callable[[], Collection[Wall]] = lambda: [],
                 icon="dungeon.png"):

        self.name = name
        self.construct_walls = construct_walls
        self.construct_objs = construct_objs
        self.h = h
        self.w = w
        self.hero_entrance = hero_entrance

        self.icon = icon

