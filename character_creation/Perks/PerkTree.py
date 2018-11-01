
from typing import List

from character_creation.Perks import PerkGroup, Perk

from my_utils.utils import flatten

class PerkTree:

    cost_factors = {1:1, 2:2.7, 3:8.8}

    def __init__(self, perk_groups: List[PerkGroup], base_cost = 100):
        self.perk_groups = perk_groups
        self.base_cost = base_cost

    def get_accessible_groups(self):
        return [pg for pg in self.perk_groups if pg.requirements_matched()]

    def accessible_perks(self):
        perks_in_accessible_groups = flatten([pg.perk_list for pg in self.get_accessible_groups()])
        not_maxed = [ p for p in perks_in_accessible_groups if p.current_level < 3]
        return not_maxed

    @property
    def all_perks(self):
        return flatten([pg.perk_list for pg in self.perk_groups])

    @property
    def total_level(self):
        return sum([p.current_level for p in self.all_perks])

    @property
    def cost_factor(self):
        tl = self.total_level
        return tl + 2 ** (tl*2/3)

    def cost_to_levelup(self, perk: Perk):
        assert perk in self.all_perks
        return perk.cost_factor*self.base_cost*self.cost_factor

