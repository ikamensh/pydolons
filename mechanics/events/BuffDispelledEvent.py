from mechanics.events import Event, BuffDetachedEvent
from mechanics.events import EventsChannels


class BuffDispelledEvent(Event):
    channel = EventsChannels.BuffDispelledChannel
    def __init__(self, game, buff, source):
        self.buff = buff
        self.source = source
        super().__init__(game)

    def check_conditions(self):
        return True

    def resolve(self):
        BuffDetachedEvent(self.game, self.buff)

    def __repr__(self):
        return f"{self.buff} was dispelled by {self.source}."