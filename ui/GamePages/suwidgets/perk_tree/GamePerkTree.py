from __future__ import annotations

from character.perks import PerkTree


class GamePerkTree:
    def __init__(self, cfg, perk_tree: PerkTree, character):
        assert perk_tree in character.perk_trees
        self.cfg = cfg
        self.perk_tree = perk_tree
        self.character = character

    def get_perks(self):
        for perk_group in self.perk_tree.perk_groups:
            for perk in perk_group.perk_list:
                yield perk.abilities
    @property
    def xp_to_levelup(self, perk):
        return self.perk_tree.cost_to_levelup(perk)

    @staticmethod
    def string_cost(cost):

        if cost >= 1e6:
            value = int(cost // 1000_000)
            rest = int((cost - value * 1000_000) // 100_000)
            if rest != 0:
                result = f"{value}.{rest}m"
            else:
                result = f"{value}m"
        elif cost > 1000:
            value = int(cost // 1000)
            rest = int((cost - value * 1000) // 100)
            if rest != 0:
                result = f"{value}.{rest}k"
            else:
                result = f"{value}k"
        else:
            result = str(cost)

        return result
