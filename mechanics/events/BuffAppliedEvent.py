from mechanics.events.Event import Event
from mechanics.events.EventsPlatform import EventsChannels
import my_globals

class BuffAppliedEvent(Event):
    channel = EventsChannels.BuffAppliedChannel

    def __init__(self, buff, unit):
        self.buff = buff
        self.unit = unit
        super().__init__()

    def check_conditions(self):
        return self.unit.alive

    def resolve(self):
        self.buff.attached_to = self.unit
        self.unit.buffs.append(self.buff)
        my_globals.the_game.turns_manager.add_buff(self.buff)

    def __repr__(self):
        return f"{self.buff} is applied on {self.unit}"
