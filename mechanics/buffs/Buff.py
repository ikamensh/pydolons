from mechanics.buffs.Ability import Ability
from game_objects.battlefield_objects.attributes import DynamicParameter
from mechanics.events import BuffExpiredEvent
import copy

class Buff(Ability):
    duration = DynamicParameter("max_duration", [BuffExpiredEvent])


    def __init__(self,duration, bonuses = None ):
        super().__init__(bonuses)
        self.max_duration = duration
        self.attached_to = None

    def clone(self):
        cpy = copy.deepcopy(self)
        cpy.reset()
        return cpy

    def reset(self):
        DynamicParameter.reset(self)

    def __repr__(self):
        return f"Buff with {self.duration}/{self.max_duration} s duration"


