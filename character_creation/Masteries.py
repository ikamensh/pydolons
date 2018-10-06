from character_creation.MasteriesEnum import MasteriesEnum, MasteriesGroups
from functools import lru_cache

class Masteries:
    def __init__(self, exp=0):
        exp_per_mastery = int(exp / len(MasteriesEnum))
        self.exp_spent = {m:exp_per_mastery for m in MasteriesEnum}

    @property
    def total_exp_spent(self):
        return sum(self.exp_spent.values())

    @staticmethod
    @lru_cache(maxsize=512)
    def increment_cost(current_level):
        if current_level <= 0:
            return 4
        else:
            if current_level <= 100:
                return int(2 + (current_level ** (5/3)/10) + Masteries.increment_cost(current_level-1))
            else:
                return int(2**(current_level/13) + Masteries.increment_cost(current_level-1))

    @staticmethod
    @lru_cache(maxsize=512)
    def cumulative_cost(current_level):
        return sum([Masteries.increment_cost(i) for i in range(current_level+1)])

    @staticmethod
    def achieved_level(exp):
        level = 0
        while exp > Masteries.cumulative_cost(level+1):
            level += 1

        return level

    @property
    def values(self):
        return { m: Masteries.achieved_level(exp) for m, exp in self.exp_spent.items()}

    def calculate_cost(self, mastery_up):

        direct_cost = self.cumulative_cost(self.values[mastery_up] + 1) - self.exp_spent[mastery_up]
        indirect_costs = {}
        for mastery in MasteriesEnum:
            coupling = MasteriesGroups.coupling(mastery, mastery_up)
            if mastery is not mastery_up and coupling > 0:
                indirect_costs[mastery] = int(direct_cost * coupling) + 1

        total_cost = direct_cost + sum(indirect_costs.values())
        return total_cost, direct_cost, indirect_costs

    def level_up(self, mastery_up):
        total_cost, direct_cost, indirect_costs = self.calculate_cost(mastery_up)
        self.exp_spent[mastery_up] += direct_cost
        for m in indirect_costs:
            self.exp_spent[m] += indirect_costs[m]

    @staticmethod
    def max_out(exp, chosen: MasteriesEnum, percentage = 0.9):
        assert 0 <= percentage <= 1
        distributed_xp = exp * (1-percentage)
        _masteries = Masteries(exp = distributed_xp)

        _masteries.exp_spent[chosen] += exp - distributed_xp
        return _masteries


    def __getitem__(self, item):
        exp = self.exp_spent[item]
        lvl = self.achieved_level(exp)
        return lvl











if __name__ == "__main__":
    # for i in range(512):
    #     print(i, Masteries.increment_cost(i))
    #
    # for m in MasteriesEnum:
    #     print(m, Masteries.requirements(m,100))


    masteries = Masteries()
    # masteries.exp_spent[MasteriesEnum.AXE] = 5000
    # masteries.exp_spent[MasteriesEnum.SWORD] = 15000
    # masteries.exp_spent[MasteriesEnum.CLUB] = 70

    print(masteries.exp_spent)
    print(masteries.values)

    while masteries.values[MasteriesEnum.CLUB]<10:
        masteries.level_up(MasteriesEnum.CLUB)
    print(masteries.level_up(MasteriesEnum.CLUB))
    print(masteries.exp_spent)
    print(masteries.values)
    while masteries.values[MasteriesEnum.AXE]<30:
        masteries.level_up(MasteriesEnum.AXE)
    print(masteries.level_up(MasteriesEnum.AXE))
    print(masteries.exp_spent)
    print(masteries.values)
    while masteries.values[MasteriesEnum.SWORD]<50:
        masteries.level_up(MasteriesEnum.SWORD)
    print(masteries.level_up(MasteriesEnum.SWORD))
    print(masteries.exp_spent)
    print(masteries.values)

