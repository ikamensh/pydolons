from mechanics.events import ActiveEvent
from mechanics.actives import ActiveTags
import copy

class Active:
    def __init__(self, targeting_cls, conditions, cost, callbacks, tags=None):
        self.targeting_cls = targeting_cls
        self.conditions = conditions
        self.cost = cost
        self.callbacks = callbacks
        self.owner = None
        self.spell = None
        self.tags = tags or []


    def check_target(self, targeting):
        if not self.conditions:
            return True
        return all((cond(self, targeting) for cond in self.conditions))

    def activate(self, targeting=None):

        if self.targeting_cls:
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
