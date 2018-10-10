from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels

class ServerOrderRecievedEvent(Event):
    channel = EventsChannels.ServerOrderRecievedChannel

    def __init__(self, fraction, x, y):
        self.fraction = fraction
        self.x = x
        self.y = y
        super().__init__()

    def check_conditions(self):
        return True

    def resolve(self):
        pass

    def __repr__(self):
        return f"player {self.fraction} has clicked {(self.x, self.y)} "
