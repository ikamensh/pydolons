from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels


class UiErrorMessageEvent(Event):
    channel = EventsChannels.UiErrorMessage

    def __init__(self, game, message):
        self.message = message
        super().__init__(game)

    def check_conditions(self):
        return True

    def resolve(self):
        pass

    def __repr__(self):
        return self.message
