from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels

class TurnEvent(Event):
    channel = EventsChannels.TurnChannel

    def __init__(self, unit, ccw):
        self.unit = unit
        self.ccw = ccw
        super().__init__(unit.game)

    def check_conditions(self):
        return True

    def resolve(self):
        turn = -1j if self.ccw else 1j
        new_turning = self.game.battlefield.unit_facings[self.unit] * turn
        self.game.battlefield.unit_facings[self.unit] = new_turning


    def __repr__(self):
        direction = "counter-clockwise" if self.ccw else "clockwise"
        return f"{self.unit} turns {direction}."
