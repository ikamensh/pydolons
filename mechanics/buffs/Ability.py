from typing import List, Callable
from mechanics.events.src.Trigger import Trigger
from game_objects import battlefield_objects as bf_objs
from game_objects import attributes

class Ability:
    def __init__(self, bonuses = None, triggers: List[Callable] = None):
        self.bonuses: List[attributes.Bonus] = bonuses
        self.triggers: List[Callable] = triggers # callable( Ability ) -> Trigger
        self.to_deactivate: List[Trigger] = []
        self.bound_to: bf_objs.Unit = None

    def apply_to(self, unit):
        self.bound_to = unit

        if self.triggers:
            for trigger in self.triggers:
                self.to_deactivate.append(trigger(self))

    def deactivate(self):
        self.bound_to = None
        for trigger in self.to_deactivate:
            trigger.deactivate()


