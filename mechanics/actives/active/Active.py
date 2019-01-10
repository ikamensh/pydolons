from __future__ import annotations
from mechanics.events import ActiveEvent
from mechanics.actives import ActiveTags
from battlefield import Cell

import traceback
from contextlib import contextmanager
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit
    from typing import ClassVar, List, Callable, Union
    from mechanics.actives import Cost
    from DreamGame import DreamGame

from mechanics.conditions.ActiveCheck import ActiveCheck
from mechanics.conditions.ActiveCondition import ActiveCondition




class Active:
    last_uid = 0

    def __init__(self, targeting_cls: ClassVar = None, conditions: List[Callable] = None, cost: Union[Cost, Callable] = None,*,
                 game: DreamGame=None, callbacks: List[Callable], tags: List[ActiveTags]=None,
                 name: str = "nameless active", cooldown = 0, simulate = None, icon: str = "fire.jpg"):
        self.name = name
        self.game = game
        self.targeting_cls = targeting_cls
        self.checker = ActiveCheck(conditions)
        self._cost = cost or Cost()
        self.callbacks = callbacks
        self.owner: Unit = None
        self.spell = None
        self.tags = tags or []
        self.simulate_callback = simulate
        self.icon = icon

        self.cooldown = cooldown
        self.remaining_cd = 0

        Active.last_uid += 1
        self.uid = Active.last_uid


    def check_target(self, target):
        failing_conditions = self.checker.not_satisfied_conds(self, target)
        # for c in failing_conditions:
        #     print(c.message(self, target))
        return len(failing_conditions) == 0

    def activate(self, target=None):
        from game_objects import battlefield_objects as bf_objs

        if self.targeting_cls in [bf_objs.Unit, bf_objs.BattlefieldObject]:
            assert isinstance(target, self.targeting_cls)
        assert self.owner is not None

        if self.affordable() and self.check_target(target):
            self.remaining_cd = self.cooldown
            self.owner.pay(self.cost)
            return ActiveEvent(self, target)
        else:
            return None

    def affordable(self):
        if self.remaining_cd > 0:
            return False
        if self.spell:
            if not self.spell.complexity_check(self.owner):
                return False
        return self.owner.can_pay(self.cost)


    def why_not_affordable(self) -> str:
        if self.spell:
            if not self.spell.complexity_check(self.owner):
                return f"This spell is too complex for {self.owner}"
        if not self.owner.can_pay(self.cost):
            return self.cost.complain(self.owner)
        if self.remaining_cd > 0:
            return "Active is on cooldown."
        else:
            return "Why not?! it is affordable."

    def why_wrong_target(self, target):
        return self.checker.complain(self, target)

    def resolve(self, targeting):
        for callback in self.callbacks:
            callback(self, targeting)

    @staticmethod
    def from_spell(spell, game=None):
        new_active = Active(spell.targeting_cls, [spell.targeting_cond] if spell.targeting_cond else None,
                            spell.cost,
                            cooldown=spell.cooldown,
                            game=game,
                            callbacks=[spell.resolve_callback],
                            tags=[ActiveTags.MAGIC])
        new_active.spell = spell

        return new_active

    @contextmanager
    def simulate(self, target):
        with self.simulate_callback(self, target):
            yield

    @property
    def tooltip_info(self):
        return {"name":f"{self.name}"}

    # the hack is here because sometimes we want to calculate cost dynamically. setting property doesn't work -
    # deepcopy throws TypeError on properties. But it does not on lambdas. Therefore _cost is either a Cost
    # object, or a lambda self: -> Cost
    @property
    def cost(self) -> Cost:
        try:
            return self._cost(self)
        except TypeError as e:
            # traceback.print_exc()
            # print(e)
            return self._cost

    def __repr__(self):
        return f"{self.name} active with {self.cost} cost ({self.tags[0] if len(self.tags) == 1 else self.tags}).".capitalize()
