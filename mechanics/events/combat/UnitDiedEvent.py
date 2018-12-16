from __future__ import annotations
from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit

class UnitDiedEvent(Event):
    channel = EventsChannels.UnitDiedChannel

    def __init__(self, unit: Unit):
        self.unit = unit
        self.killer: Unit = unit.last_damaged_by
        super().__init__(unit.game, logging=True)

    def check_conditions(self):
        return self.unit.alive

    def resolve(self):
        self.game.unit_died(self.unit)

    def __repr__(self):
        if self.killer:
            if self.killer != self.unit:
                return "{} is killed by {}".format(self.unit, self.killer)
            else:
                return "{} commits suicide.".format(self.unit)
        else:
            return "{} dies.".format(self.unit)
