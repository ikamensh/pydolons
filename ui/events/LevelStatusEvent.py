from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels


class LevelStatusEvent(Event):
    channel = EventsChannels.LevelStatus

    def __init__(self, game, status):
        self.status = status
        super().__init__(game)

    def check_conditions(self):
        return True

    def resolve(self):
        pass

    def __repr__(self):
        return f"Level complete is {self.status}"
