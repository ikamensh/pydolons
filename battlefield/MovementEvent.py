from mechanics.events.Event import Event
from mechanics.events.EventsPlatform import EventsChannels

class MovementEvent(Event):
    channel = EventsChannels.MovementChannel

    def __init__(self, battlefield, unit, cell_to):
        self.battlefield = battlefield
        self.unit = unit
        self.cell_from = battlefield.unit_locations[unit]
        self.cell_to = cell_to
        self.unit.readiness -= 0.5
        super().__init__()

    def check_conditions(self):
        return self.battlefield.get_unit_at(self.cell_to) is None

    def resolve(self):
        self.unit.readiness -= 0.5
        self.battlefield.move(self.unit, self.cell_to)

    def __repr__(self):
        return "{} moves from {} to {}".format(self.unit, self.cell_from, self.cell_to)