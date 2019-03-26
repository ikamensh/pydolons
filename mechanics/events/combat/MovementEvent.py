from __future__ import annotations
from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
from battlefield import Cell
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit

class MovementEvent(Event):
    channel = EventsChannels.MovementChannel

    def __init__(self, unit: Unit, cell_to: Union[Cell, complex], fire=True):
        self.unit = unit
        game = unit.game
        self.bf = game.bf
        self.cell_from = unit.cell
        self.cell_to = Cell.maybe_complex(cell_to)
        super().__init__(game, fire=fire, logging=True)

    def check_conditions(self):
        return all((self.unit.alive,
                   not self.cell_to in self.game.bf.walls,
                   self.cell_to in self.game.bf.all_cells))

    def resolve(self):
        self.unit.cell = self.cell_to

    def __repr__(self):
        return f"{self.unit} moves from {self.cell_from} to {self.cell_to}"




