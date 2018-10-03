from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
import my_context
# from ui.gui_util.gamechanel import gamechanel

class ActiveEvent(Event):
    channel = EventsChannels.ActiveChannel

    def __init__(self, active, targeting):
        self.active = active
        self.targeting = targeting
        super().__init__()

    def check_conditions(self):
        return all([self.active.owner.alive, self.active.owner_can_afford_activation(),
                   self.active.check_target(self.targeting)])

    def resolve(self):
        # print(type(self.active))
        # print('self.targeting dir :\n',type(self.targeting))
        self.active.resolve(self.targeting)
        # gamechanel.sendMessage({'event':'ActiveEvent','target':self.targeting, 'active':self.active})

    def __repr__(self):
        return f"{self.active.owner} activates {self.active}, {self.targeting}"
