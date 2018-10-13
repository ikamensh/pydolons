from mechanics.events import Event
from mechanics.events import EventsChannels

class BuffAppliedEvent(Event):
    channel = EventsChannels.BuffAppliedChannel

    def __init__(self, buff, unit):
        self.buff = buff
        self.unit = unit
        super().__init__(unit.game)

    def check_conditions(self):
        return self.unit.alive

    def resolve(self):
        self.unit.add_buff(self.buff)
        self.game.turns_manager.add_buff(self.buff)

    def __repr__(self):
        return f"{self.buff} is applied on {self.unit}"
