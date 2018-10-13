from mechanics.events import Event, BuffDetachedEvent
from mechanics.events import EventsChannels


class BuffExpiredEvent(Event):
    channel = EventsChannels.BuffExpiredChannel

    def __init__(self, game, buff):
        self.buff = buff
        super().__init__(game)

    def check_conditions(self):
        return self.buff.duration <= 0

    def resolve(self):
        BuffDetachedEvent(self.game, self.buff)

    def __repr__(self):
        return f"{self.buff} has expired."