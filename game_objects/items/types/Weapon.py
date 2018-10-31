from mechanics.damage.Damage import Damage
from game_objects.items import WearableItem, ItemTypes
from mechanics.chances.CritHitGrazeMiss import ImpactChances

import copy

class Weapon(WearableItem):
    def __init__(self, name, damage, chances=None, atb_factor=1., *,max_durability=None,
                 mastery=None, blueprint=None, material=None,quality=None, actives=None,
                 is_ranged,
                 game):
        super().__init__(name, ItemTypes.WEAPON, blueprint=blueprint, quality=quality,
                         material=material, max_durability=max_durability, actives = actives,
                         game=game)
        assert isinstance(damage, Damage)
        if chances:
            assert isinstance(chances, ImpactChances)

        self._damage = damage
        self.chances = chances or ImpactChances(0.05, 0.4, 0.5)
        self.atb_factor = atb_factor
        self.mastery = mastery
        self.is_ranged = is_ranged

    @property
    def damage(self):
        if self.max_durability is None:
            return copy.copy(self._damage)

        return Damage(self._damage.amount * self.durability_factor, self._damage.type)


    def __repr__(self):
        return f"{self.name} dealing {self.damage}"