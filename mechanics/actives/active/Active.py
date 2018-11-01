from __future__ import annotations
from mechanics.events import ActiveEvent
from mechanics.actives import ActiveTags
from battlefield import Cell
import copy
from contextlib import contextmanager
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game_objects.battlefield_objects import Unit
    from typing import ClassVar, List, Callable, Union
    from mechanics.actives import Cost
    from DreamGame import DreamGame

class Active:
    last_uid = 0

    def __init__(self, targeting_cls: ClassVar = None, conditions: List[Callable] = None, cost: Union[Cost, Callable] = None,*,
                 game: DreamGame=None, callbacks: List[Callable], tags: List[ActiveTags]=None,
                 name: str = "nameless active",simulate = None, icon: str = "fire.jpg"):
        self.name = name
        self.game = game
        self.targeting_cls = targeting_cls
        self.conditions = conditions or []
        self._cost = cost or Cost()
        self.callbacks = callbacks
        self.owner: Unit = None
        self.spell = None
        self.tags = tags or []
        self.simulate_callback = simulate
        self.icon = icon

        Active.last_uid += 1
        self.uid = Active.last_uid


    def check_target(self, targeting):
        if not self.conditions:
            return True
        return all((cond(self, targeting) for cond in self.conditions))

    def activate(self, targeting=None):
        from game_objects import battlefield_objects as bf_objs

        if self.targeting_cls in [Cell, bf_objs.Unit, bf_objs.BattlefieldObject]:
            assert isinstance(targeting, self.targeting_cls)
        assert self.owner is not None

        if self.owner_can_afford_activation() and self.check_target(targeting):
            cpy = copy.copy(self)
            cpy._cost = copy.deepcopy(cpy._cost)
            cpy.spell = copy.deepcopy(cpy.spell)
            cpy.game = self.owner.game
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
    def from_spell(spell, game=None):
        new_active = Active(spell.targeting_cls, [spell.targeting_cond],
                            spell.cost,
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
    def cost(self):
        try:
            return self._cost(self)
        except TypeError:
            return self._cost

    def __repr__(self):
        return f"{self.name} active with {self.cost} cost ({self.tags[0] if len(self.tags) == 1 else self.tags}).".capitalize()
