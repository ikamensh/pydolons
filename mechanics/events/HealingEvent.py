from __future__ import annotations
from mechanics.events import EventsChannels
from mechanics.events.src.Event import Event
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit, BattlefieldObject

class HealingEvent(Event):
    channel = EventsChannels.HealingChannel

    def __init__(self, healing_amount: float, target: BattlefieldObject, *, source: Unit=None):
        self.source = source
        self.target = target
        self.healing_amount = healing_amount
        super().__init__(target.game)

    def check_conditions(self):
        return self.target.alive and self.healing_amount > 0

    def resolve(self):
        self.target.health += self.healing_amount

    def __repr__(self):
        return f"{self.target} is healed for {self.healing_amount}" \
               + f"by {self.source}" if self.source else ""
