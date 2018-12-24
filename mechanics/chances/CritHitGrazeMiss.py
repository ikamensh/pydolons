from __future__ import annotations
from my_utils.named_enums import NameEnum, auto
from mechanics.chances.ChanceCalculator import ChanceCalculator
from dataclasses import dataclass

class ImpactFactor(NameEnum):
    CRIT = auto()
    HIT = auto()
    GRAZE = auto()
    MISS = auto()


@dataclass(frozen=True)
class ImpactChances:
    crit:float
    hit:float
    graze:float

    @property
    def sequential_hit_chance(self):
        return (1-self.crit)*self.hit

    @property
    def sequential_graze_chance(self):
        return (1-self.crit)*(1-self.hit)*self.graze

    def actual(self, precision, evasion):
        return self._calc_chances(self, precision, evasion)

    def roll_impact(self, *, random) -> ImpactFactor:
        chance_crit, chance_hit, chance_graze = self
        if random.random() < chance_crit:
            return ImpactFactor.CRIT
        elif random.random() < chance_hit:
            return ImpactFactor.HIT
        elif random.random() < chance_graze:
            return ImpactFactor.GRAZE
        else:
            return ImpactFactor.MISS

    @staticmethod
    def _calc_chances(initial_chances: ImpactChances, precision, evasion) -> ImpactChances:
        chance_crit, chance_hit, chance_graze = [ChanceCalculator.chance(c, precision, evasion) for c in
                                                 initial_chances]
        return ImpactChances(chance_crit, chance_hit, chance_graze)

    def __iter__(self):
        return iter((self.crit, self.hit, self.graze))

    def __repr__(self):
        return f"crit/hit/graze chances: {100*self.crit:.2f} / {100*self.sequential_hit_chance:.2f} / {100*self.sequential_graze_chance:.2f}%"







if __name__ == "__main__":
    ic = ImpactChances(0.05, 0.5,0.5)
    print(ic)

    ic = ImpactChances(0.05, 0.75, 0.5)
    print(ic)

    ic = ImpactChances(0.01, 0.5, 0.6)
    print(ic)
    ic2 = ic.calc_chances(ic, 0, 50)
    print(ic2)