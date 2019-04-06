from __future__ import annotations

from character.perks import PerkTree
from character.perks.everymans_perks.group_attrib import attr_perk_names as attr_names
from character.perks.everymans_perks.group_param import attr_perk_names as param_names
from game_objects.battlefield_objects import CharAttributes, enum_to_abbrev

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from character.Character import Character


class GamePerkTree:
    def __init__(self, perk_tree: PerkTree, character: Character):
        assert perk_tree in character.perk_trees
        self.perk_tree = perk_tree
        self.character = character
        self.perks = {}
        self.perks_info = {}
        self.setUpPerkParams()

    def get_perks(self):
        for perk_group in self.perk_tree.perk_groups:
            for perk in perk_group.perk_list:
                yield perk

    def setUpPerkParams(self):
        cha_attributes = [CharAttributes.STREINGTH,
                          CharAttributes.AGILITY,
                          CharAttributes.ENDURANCE,
                          CharAttributes.PERCEPTION,
                          CharAttributes.INTELLIGENCE,
                          CharAttributes.CHARISMA]
        cha_params = [CharAttributes.HEALTH,
                          CharAttributes.MANA,
                          CharAttributes.STAMINA,
                          CharAttributes.INITIATIVE]
        cha_atrs_names = [attr_names(attr) for attr in cha_attributes]
        cha_atrs_names = cha_atrs_names + [param_names(attr) for attr in cha_params]
        cha_atrs_abrv = [enum_to_abbrev[attr] for attr in cha_attributes]
        cha_atrs_abrv = cha_atrs_abrv[0:6] + ['hel', 'man', 'sta', 'ini']
        l = len(cha_atrs_names)
        for i in range(l):
            for perk in self.get_perks():
                if perk.name == cha_atrs_names[i]:
                    self.perks[cha_atrs_abrv[i]] = perk
        self.perks_info = {'perk_'+abrv: perk.tooltip_info for abrv, perk in self.perks.items()}

    def xp_to_levelup(self, perk):
        return self.perk_tree.cost_to_levelup(perk)

    def xp_to_text(self, perk):
        if perk.current_level != 3:
            return self.string_cost(self.xp_to_levelup(perk))
        else:
            return "^maxed^"
    @property
    def spent_xp(self):
        return self.string_cost(self.perk_tree.spent_xp)

    def perk_up(self, perk):
        self.perk_tree.spent_xp += self.xp_to_levelup(perk)
        perk.current_level += 1

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


