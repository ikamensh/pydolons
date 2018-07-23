from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
import my_globals

class ActiveEvent(Event):
    channel = EventsChannels.ActiveChannel

    def __init__(self, active, targeting):
        self.active = active
        self.targeting = targeting
        active.owner.readiness -= active.cost.readiness / 2
        active.cost.readiness /= 2
        super().__init__()

    def check_conditions(self):
        return all([self.active.owner.alive, self.active.owner_can_afford_activation(),
                   self.active.targeting_cond(self.active, self.targeting)])

    def resolve(self):
        self.active.resolve(self.targeting)

    def __repr__(self):
        return f"{self.active.owner} activates {self.active}, {self.targeting}"