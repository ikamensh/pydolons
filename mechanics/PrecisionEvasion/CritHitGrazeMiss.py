from utils.named_enums import NameEnum, auto
from mechanics.PrecisionEvasion.ChanceCalculator import ChanceCalculator
import random
from collections import namedtuple

ImpactChances = namedtuple("ImpactChances", "crit hit graze")


class ImpactFactor(NameEnum):
    CRIT = auto()
    HIT = auto()
    GRAZE = auto()
    MISS = auto()

protection_coef = {
    ImpactFactor.CRIT:0.7,
    ImpactFactor.HIT:1.0,
    ImpactFactor.GRAZE:1.4
}

effect_coef = {
    ImpactFactor.CRIT:1.5,
    ImpactFactor.HIT: 1,
    ImpactFactor.GRAZE: 0.66
}


# Optimizable - do not calculate chance before needed.
class ImpactCalculator:
    @staticmethod
    def roll_impact(chances, precision, evasion):
        assert isinstance(chances, ImpactChances)
        chance_crit , chance_hit, chance_graze = [ChanceCalculator.chance(c, precision, evasion) for c in chances]
        if random.random() < chance_crit:
            return ImpactFactor.CRIT
        elif random.random() < chance_hit:
            return ImpactFactor.HIT
        elif random.random() < chance_graze:
            return ImpactFactor.GRAZE
        else:
            return ImpactFactor.MISS
