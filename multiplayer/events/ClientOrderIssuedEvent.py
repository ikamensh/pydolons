from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels

class ClientOrderIssuedEvent(Event):
    channel = EventsChannels.ClientOrderIssuedChannel

    def __init__(self, game, unit_uid, active_uid, target):
        self.unit_uid = unit_uid
        self.active_uid = active_uid
        self.target = target
        super().__init__(game)

    def check_conditions(self):
        return True

    def resolve(self):
        pass

    def __repr__(self):
        return f"COI order: unit:{self.unit_uid} active:{self.active_uid} target:{self.target} "
