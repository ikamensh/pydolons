from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels

class TimePassedEvent(Event):
    channel = EventsChannels.TimePassedChannel

    def __init__(self, game, dt):
        self.dt = dt
        super().__init__(game)

    def check_conditions(self):
        return True

    def resolve(self):
        pass

    def __repr__(self):
        return f"{self.dt} time has passed."
