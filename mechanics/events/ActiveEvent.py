from __future__ import annotations
from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mechanics.actives import Active

class ActiveEvent(Event):
    channel = EventsChannels.ActiveChannel

    def __init__(self, active: "Active", targeting):
        self.active = active
        self.targeting = targeting
        super().__init__(active.game)

    def check_conditions(self):
        return True

    def resolve(self):
        # print(type(self.active))
        # print('self.targeting dir :\n',type(self.targeting))
        self.active.resolve(self.targeting)

    def __repr__(self):
        return f"{self.active.owner} activates {self.active}, {self.targeting}"
