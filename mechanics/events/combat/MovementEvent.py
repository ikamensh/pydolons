from __future__ import annotations
from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
from battlefield import Cell
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit

class MovementEvent(Event):
    channel = EventsChannels.MovementChannel

    def __init__(self, unit: Unit, cell_to: Union[Cell, complex]):
        self.unit = unit
        if self.check_conditions():
            game = unit.game
            self.battlefield = game.battlefield
            self.cell_from = self.battlefield.unit_locations[unit]
            self.cell_to = Cell.maybe_complex(cell_to)
            super().__init__(game)

    def check_conditions(self):
        return self.unit.alive

    def resolve(self):
        self.battlefield.move(self.unit, self.cell_to)

    def __repr__(self):
        return "{} moves from {} to {}".format(self.unit, self.cell_from, self.cell_to)




