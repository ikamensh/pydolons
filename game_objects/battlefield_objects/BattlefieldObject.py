from abc import ABC
from battlefield import Cell
from exceptions import PydolonsError
from typing import Union


class BattlefieldObject(ABC):

    size = 3
    last_uid = 0

    def __init__(self, cell=None):
        BattlefieldObject.last_uid += 1
        self.uid = BattlefieldObject.last_uid
        self._cell = None
        if cell is not None:
            self.cell = cell

    uid = None
    is_obstacle = None
    melee_evasion = 0
    alive = None
    game = None
    health = None

    @property
    def cell(self) -> Cell:
        return self._cell

    @cell.setter
    def cell(self, value: Union[Cell, complex]):
        if isinstance(value, complex):
            self._cell = Cell.from_complex(value)
        elif isinstance(value, Cell):
            self._cell = value
        else:
            raise PydolonsError(
                f"Obj.cell attribute can only be assigned with complex or Cell types."
                f"Actual passed type: {type(value)}")

    def lose_health(self, amount, source=None):
        raise NotImplementedError
