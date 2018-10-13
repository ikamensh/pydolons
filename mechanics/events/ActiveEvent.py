from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels

class ActiveEvent(Event):
    channel = EventsChannels.ActiveChannel

    def __init__(self, game, active, targeting):
        self.active = active
        self.targeting = targeting
        super().__init__(game)

    def check_conditions(self):
        return all([self.active.owner.alive, self.active.owner_can_afford_activation(),
                   self.active.check_target(self.targeting)])

    def resolve(self):
        # print(type(self.active))
        # print('self.targeting dir :\n',type(self.targeting))
        self.active.resolve(self.targeting)

    def __repr__(self):
        return f"{self.active.owner} activates {self.active}, {self.targeting}"
