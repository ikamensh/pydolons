from __future__ import annotations

from character.masteries.MasteriesEnumSimple import MasteriesGroups

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from character.Character import Character


class GameMasteries:
    def __init__(self, character):
        self.character: Character = character
        self.masteries = {}
        self.masteries_info = {}
        pass

    def setUpMasteries(self):
        self.masteries = dict(zip([m.name.lower() for m in MasteriesGroups.all_magic+MasteriesGroups.all_battle], MasteriesGroups.all_magic+MasteriesGroups.all_battle))
        self.masteries_info = {'mastery_'+name:mastery.tooltip_info for name, mastery in self.masteries.items()}

    def mastery_up(self, mastery):
        self.character.increase_mastery(mastery)

    def get_perc(self, total, current):
        return current / total

    def mastery_value(self, mastery):
        return str(self.character.masteries.values[mastery])

    def mastery_prec(self, mastery):
        total, direct, mm = self.character.masteries.calculate_cost(mastery)
        return self.get_perc(total, direct), mm

    def string_cost(self, cost):
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

    @property
    def spent_xp(self):
        return self.string_cost(self.character.masteries.total_exp_spent)
