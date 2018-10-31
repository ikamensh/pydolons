from __future__ import annotations
from mechanics.events import Event
from mechanics.events import EventsChannels
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mechanics.buffs import Buff

class BuffDetachedEvent(Event):
    channel = EventsChannels.BuffDetachedChannel

    def __init__(self, buff):
        self.buff = buff
        super().__init__(buff.bound_to.game)

    def check_conditions(self):
        return True

    def resolve(self):
        self.buff.bound_to.remove_buff(self.buff)
        self.game.turns_manager.remove_buff(self.buff)

    def __repr__(self):
        return f"{self.buff} has detached."
