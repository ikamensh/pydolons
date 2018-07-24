from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
from battlefield.Facing import Facing

class TurnEvent(Event):
    channel = EventsChannels.MovementChannel

    def __init__(self, battlefield, unit, ccw):
        self.battlefield = battlefield
        self.unit = unit
        self.ccw = ccw
        super().__init__()

    def check_conditions(self):
        return True

    def resolve(self):
        turn = 1j if self.ccw else -1j
        self.battlefield.unit_facings[self.unit] *= turn

    def __repr__(self):
        direction = "counter-clockwise" if self.ccw else "clockwise"
        return f"{self.unit} facing {Facing.to_str[self.battlefield.unit_facings[self.unit]]} turns {direction}."