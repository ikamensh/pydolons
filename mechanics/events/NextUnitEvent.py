from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels

class NextUnitEvent(Event):
    channel = EventsChannels.NextUnitChannel

    def __init__(self, game, unit):
        self.unit = unit
        super().__init__()

    def check_conditions(self):
        return True

    def resolve(self):
        pass

    def __repr__(self):
        return f"{self.unit} is now making turn."
