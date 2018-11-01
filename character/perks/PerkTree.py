
from typing import List

from character.perks import PerkGroup, Perk

from my_utils.utils import flatten

import math

class PerkTree:

    cost_factors = {1:1, 2:3, 3:7}

    def __init__(self, perk_groups: List[PerkGroup], base_cost = 100):
        self.perk_groups = perk_groups
        self.base_cost = base_cost

    def get_accessible_groups(self) -> List[PerkGroup]:
        return [pg for pg in self.perk_groups if pg.requirements_matched()]

    def accessible_perks(self) -> List[Perk]:
        perks_in_accessible_groups = flatten([pg.perk_list for pg in self.get_accessible_groups()])
        not_maxed = [ p for p in perks_in_accessible_groups if p.current_level < 3]
        return not_maxed

    @property
    def all_perks(self) -> List[Perk]:
        return flatten([pg.perk_list for pg in self.perk_groups])

    @property
    def total_level(self) -> int:
        return sum([p.current_level for p in self.all_perks])

    @property
    def cost_growth(self) -> float:
        tl = self.total_level
        return 2 ** (tl*11/13)

    def cost_to_levelup(self, perk: Perk) -> int:
        assert perk in self.all_perks
        precise_cost =  perk.cost_factor * self.base_cost * self.cost_growth * \
                        ( self.cost_factors[perk.current_level+1] ** (1 + self.total_level/60) )
        log10 = int( math.log10(precise_cost) )

        base = 10 ** (log10-1)
        return int( precise_cost // base * base )

    @property
    def all_abils(self):
        return flatten([p.abils for p in self.all_perks])




if __name__ == "__main__":
    for i in range(25):
        tl = i
        print(i, tl/2 + 2 ** (tl*4/3))