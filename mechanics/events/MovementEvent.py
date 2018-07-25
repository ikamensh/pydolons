from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
from battlefield import Cell
import my_context

class MovementEvent(Event):
    channel = EventsChannels.MovementChannel

    def __init__(self, unit, cell_to):
        self.battlefield = my_context.the_game.battlefield
        self.unit = unit
        self.cell_from = self.battlefield.unit_locations[unit]
        self.cell_to = Cell.maybe_complex(cell_to)
        super().__init__()

    def check_conditions(self):
        return self.battlefield.get_unit_at(self.cell_to) is None

    def resolve(self):
        self.battlefield.move(self.unit, self.cell_to)

    def __repr__(self):
        return "{} moves from {} to {}".format(self.unit, self.cell_from, self.cell_to)