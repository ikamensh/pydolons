from mechanics.buffs.Ability import Ability
from game_objects.attributes import DynamicParameter
from mechanics.events import BuffExpiredEvent



class Buff(Ability):
    duration = DynamicParameter("max_duration", [BuffExpiredEvent])


    def __init__(self, duration: float, bonus = None, triggers_factories = None, source = None, name="nameless"):
        super().__init__(bonus, triggers_factories, name)
        self.max_duration = duration
        self.source = source

    def reset(self):
        DynamicParameter.reset(self)

    def __repr__(self):
        return f"Buff {self.name}: {self.duration}/{self.max_duration} s left; on {self.bound_to}"


