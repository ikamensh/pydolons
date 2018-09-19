from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
from battlefield.Facing import Facing
import my_context


class TurnEvent(Event):
    channel = EventsChannels.MovementChannel

    def __init__(self, unit, ccw):
        self.unit = unit
        self.ccw = ccw
        self.battlefield = my_context.the_game.battlefield
        super().__init__()

    def check_conditions(self):
        return True

    def resolve(self):
        turn = 1j if self.ccw else -1j
        old_turning = self.battlefield.unit_facings[self.unit]
        new_turning = self.battlefield.unit_facings[self.unit] * turn
        self.battlefield.unit_facings[self.unit] = new_turning

    def __repr__(self):
        direction = "counter-clockwise" if self.ccw else "clockwise"
        return f"{self.unit} facing {Facing.to_str[self.battlefield.unit_facings[self.unit]]} turns {direction}."