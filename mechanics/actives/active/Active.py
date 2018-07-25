from mechanics.events import ActiveEvent
from mechanics.actives import ActiveTags
from battlefield import Cell
import copy

class Active:
    last_uid = 0

    def __init__(self, targeting_cls, conditions, cost, callbacks, tags=None, name = "Mysterious"):
        self.name = name
        self.targeting_cls = targeting_cls
        self.conditions = conditions
        self.cost = cost
        self.callbacks = callbacks
        self.owner = None
        self.spell = None
        self.tags = tags or []

        Active.last_uid += 1
        self.uid = Active.last_uid


    def check_target(self, targeting):
        if not self.conditions:
            return True
        return all((cond(self, targeting) for cond in self.conditions))

    def activate(self, targeting=None):

        if self.targeting_cls is Cell:
            assert isinstance(targeting, self.targeting_cls)
        assert self.owner is not None

        if self.owner_can_afford_activation() and self.check_target(targeting):
            cpy = copy.copy(self)
            cpy.cost = copy.copy(cpy.cost)
            cpy.spell = copy.copy(cpy.spell)
            self.owner.pay(self.cost)
            ActiveEvent(cpy, targeting)

    def owner_can_afford_activation(self):
        if self.spell:
            if not self.spell.complexity_check(self.owner):
                return False
        return self.owner.can_pay(self.cost)

    def resolve(self, targeting):
        for callback in self.callbacks:
            callback(self, targeting)

    @staticmethod
    def from_spell(spell):
        new_active = Active(spell.targeting_cls, [spell.targeting_cond],
                            spell.cost, [spell.resolve_callback], [ActiveTags.MAGIC])
        new_active.spell = spell

        return new_active

    def __repr__(self):
        return f"{self.name} active with {self.cost} cost ({self.tags[0] if len(self.tags) == 1 else self.tags}).".capitalize()
