from __future__ import annotations
from mechanics.events import Event, BuffDetachedEvent
from mechanics.events import EventsChannels
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mechanics.buffs import Buff
    from game_objects.battlefield_objects import Unit


class BuffDispelledEvent(Event):
    channel = EventsChannels.BuffDispelledChannel

    def __init__(self, buff: Buff, source: Unit):
        self.buff = buff
        self.source = source
        super().__init__(self.buff.bound_to.game)

    def check_conditions(self):
        return True

    def resolve(self):
        BuffDetachedEvent(self.buff)

    def __repr__(self):
        return f"{self.buff} was dispelled by {self.source}."
