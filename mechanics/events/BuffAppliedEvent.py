from mechanics.events import Event
from mechanics.events import EventsChannels
import my_context

class BuffAppliedEvent(Event):
    channel = EventsChannels.BuffAppliedChannel

    def __init__(self, buff, unit):
        self.buff = buff
        self.unit = unit
        super().__init__()

    def check_conditions(self):
        return self.unit.alive

    def resolve(self):
        self.unit.add_buff(self.buff)
        my_context.the_game.turns_manager.add_buff(self.buff)

    def __repr__(self):
        return f"{self.buff} is applied on {self.unit}"
