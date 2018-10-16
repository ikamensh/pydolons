from __future__ import annotations
from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit

class NextUnitEvent(Event):
    channel = EventsChannels.NextUnitChannel

    def __init__(self, unit: Unit):
        self.unit = unit
        super().__init__(unit.game)

    def check_conditions(self):
        return True

    def resolve(self):
        pass

    def __repr__(self):
        return f"{self.unit} is now making turn."
