from mechanics.events.src.Trigger import Trigger

from typing import List, Callable
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit
    from game_objects.attributes import Bonus


class Ability:
    def __init__(self, bonuses = None, triggers: List[Callable] = None):
        self.bonuses: List[Bonus] = bonuses
        self.triggers: List[Callable] = triggers # callable( Ability ) -> Trigger
        self.to_deactivate: List[Trigger] = []
        self.bound_to: Unit = None

    def apply_to(self, unit):
        self.bound_to = unit

        if self.triggers:
            for trigger in self.triggers:
                self.to_deactivate.append(trigger(self))

    def deactivate(self):
        self.bound_to = None
        for trigger in self.to_deactivate:
            trigger.deactivate()


