from __future__ import annotations
from mechanics.events.src.Trigger import Trigger

from typing import List, Callable
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit
    from game_objects.attributes import Bonus


class Ability:
    def __init__(
            self,
            bonus: Bonus = None,
            trigger_factories: List[Callable] = None,
            name="Nameless ability"):
        self.bonus = bonus
        # callable( Ability ) -> Trigger
        self.trigger_factories = trigger_factories
        self.to_deactivate: List[Trigger] = []
        self.bound_to: Unit = None
        self.name = name

    def apply_to(self, unit):
        self.bound_to = unit

        if self.trigger_factories:
            for trigger in self.trigger_factories:
                self.to_deactivate.append(trigger(self))

    def deactivate(self):
        self.bound_to = None
        for trigger in self.to_deactivate:
            trigger.deactivate()

    def rpg_description(self):
        descr = f"Bonuses: {self.bonus}"
        if self.trigger_factories:
            for tf in self.trigger_factories:
                descr += "\n" + repr(tf)

    def __repr__(self):
        return f"{self.name} belonging to {self.bound_to}"
