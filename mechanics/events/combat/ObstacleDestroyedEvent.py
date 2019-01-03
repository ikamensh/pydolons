from __future__ import annotations
from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Obstacle, Unit


class ObstacleDestroyedEvent(Event):
    channel = EventsChannels.ObstacleDestroyedChannel

    def __init__(self, unit: Obstacle):
        self.unit = unit
        self.killer: Unit = unit.last_damaged_by
        super().__init__(unit.game)

    def check_conditions(self):
        return self.unit.alive

    def resolve(self):
        self.unit.alive = False
        self.game.obstacle_destroyed(self.unit)

    def __repr__(self):
        if self.killer:
            return "{} was destroyed by {}".format(self.unit, self.killer)
        else:
            return "{} was destroyed.".format(self.unit)
