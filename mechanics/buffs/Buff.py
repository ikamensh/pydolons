from mechanics.buffs.Ability import Ability

class Buff(Ability):
    def __init__(self, attributes_dict, duration):
        super().__init__(attributes_dict)
        self.duration = duration
        self.time_left = duration
