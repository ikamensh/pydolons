from __future__ import annotations
from mechanics.events import Event
from mechanics.events import EventsChannels
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mechanics.buffs import Buff
    from game_objects.battlefield_objects import Unit


class BuffAppliedEvent(Event):
    channel = EventsChannels.BuffAppliedChannel

    def __init__(self, buff: Buff, unit: Unit):
        self.buff = buff
        self.unit = unit
        super().__init__(unit.game, logging=True)

    def check_conditions(self):
        return self.unit.alive

    def resolve(self):
        self.unit.add_buff(self.buff)
        self.game.turns_manager.add_buff(self.buff)

    def __repr__(self):
        return f"{self.buff} is applied on {self.unit}"
