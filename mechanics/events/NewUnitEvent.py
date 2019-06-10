from __future__ import annotations
from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit


class NewUnitEvent(Event):
    channel = EventsChannels.NewUnitChannel

    def __init__(self, unit: Unit):
        self.unit = unit
        super().__init__(unit.game, logging=True)

    def check_conditions(self):
        return self.unit.alive

    def resolve(self):
        self.game.add_unit(self.unit)

    def __repr__(self):
        return f"{self.unit} was added."
