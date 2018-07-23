from dataclasses import dataclass
from game_objects.battlefield_objects import Unit
from battlefield.Battlefield import Cell

@dataclass()
class CellTargeting:
    cell: Cell

@dataclass()
class SingleUnitTargeting:
    unit: Unit




