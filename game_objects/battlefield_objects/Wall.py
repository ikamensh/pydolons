from battlefield import Cell
from exceptions import PydolonsError
from typing import Union

class Wall:
    def __init__(self, cell: Union[Cell, complex], icon: str = 'wall.png'):
        self.cell = cell
        self.icon = icon

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
                f"Actual passed type: {type(value)}"
            )
