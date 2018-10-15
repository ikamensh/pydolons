from mechanics.buffs.Ability import Ability
from game_objects.attributes import DynamicParameter
from mechanics.events import BuffExpiredEvent

class Buff(Ability):
    duration = DynamicParameter("max_duration", [BuffExpiredEvent])


    def __init__(self,duration, bonuses = None, triggers = None):
        super().__init__(bonuses, triggers)
        self.max_duration = duration

    def reset(self):
        DynamicParameter.reset(self)

    def __repr__(self):
        if self.bound_to:
            return f"Buff with {self.duration}/{self.max_duration} s duration"
        else:
            return "Abstract Buff..."


