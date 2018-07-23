from mechanics.events import ActiveEvent
import copy

class Active:
    def __init__(self, targeting_cls, targeting_cond, cost, callbacks):
        self.targeting_cls = targeting_cls
        self.targeting_cond = targeting_cond
        self.cost = cost
        self.callbacks = callbacks
        self.owner = None
        self.spell = None

    def assign_to_unit(self, new_owner):
        self.owner = new_owner


    def activate(self, user_targeting):
        assert isinstance(user_targeting, self.targeting_cls)
        assert self.owner is not None

        if self.targeting_cond(self, user_targeting):
            cpy = copy.copy(self)
            cpy.cost = copy.copy(cpy.cost)
            cpy.spell = copy.copy(cpy.spell)
            ActiveEvent(cpy, user_targeting)

    def owner_can_afford_activation(self):
        if self.spell:
            if not self.spell.complexity_check(self.owner):
                return False
        return self.owner.can_pay(self.cost)

    def resolve(self, targeting):
        self.owner.pay(self.cost)
        for callback in self.callbacks:
            callback(self, targeting)

    @staticmethod
    def from_spell(spell):
        new_active = Active(spell.targeting_cls, spell.targeting_cond,
                            spell.costs, [spell.resolve_callback])
        new_active.spell = spell
        return new_active
