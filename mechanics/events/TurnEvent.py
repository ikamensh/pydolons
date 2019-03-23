from __future__ import annotations
from mechanics.events.src.Event import Event
from mechanics.events import EventsChannels
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit

class TurnEvent(Event):
    channel = EventsChannels.TurnChannel

    def __init__(self, unit: Unit, ccw: bool):
        self.unit = unit
        self.ccw = ccw
        super().__init__(unit.game)

    def check_conditions(self):
        return True

    def resolve(self):
        turn = -1j if self.ccw else 1j
        self.unit.facing *= turn


    def __repr__(self):
        direction = "counter-clockwise" if self.ccw else "clockwise"
        return f"{self.unit} turns {direction}."
