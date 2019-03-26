from __future__ import annotations
from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit

from game_objects import battlefield_objects


class UnitDiedEvent(Event):
    channel = EventsChannels.UnitDiedChannel

    def __init__(self, unit: Unit):
        self.unit = unit
        self.killer: Unit = unit.last_damaged_by
        self.corpse = None
        super().__init__(unit.game, logging=True)

    def check_conditions(self):
        return self.unit.alive

    def resolve(self):
        self.game.unit_died(self.unit)
        self.corpse = battlefield_objects.Corpse(self.unit)
        self.game.add_obstacle(self.corpse)

    def __repr__(self):
        if self.killer:
            if self.killer != self.unit:
                return f"{self.unit} is killed by {self.killer}"
            else:
                return f"{self.unit} commits suicide."
        else:
            return f"{self.unit} dies."
