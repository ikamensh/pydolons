from my_utils.named_enums import NameEnum, auto
from mechanics.chances.ChanceCalculator import ChanceCalculator
import my_context
from collections import namedtuple

ImpactChances = namedtuple("ImpactChances", "crit hit graze")


class ImpactFactor(NameEnum):
    CRIT = auto()
    HIT = auto()
    GRAZE = auto()
    MISS = auto()


# Optimizable - do not calculate chance before needed.
class ImpactCalculator:
    @staticmethod
    def roll_impact(chances, precision, evasion):
        assert isinstance(chances, ImpactChances)
        chance_crit , chance_hit, chance_graze = ImpactCalculator.calc_chances(chances, precision, evasion)
        if my_context.random.random() < chance_crit:
            return ImpactFactor.CRIT
        elif my_context.random.random() < chance_hit:
            return ImpactFactor.HIT
        elif my_context.random.random() < chance_graze:
            return ImpactFactor.GRAZE
        else:
            return ImpactFactor.MISS

    @staticmethod
    def calc_chances(initial_chances, precision, evasion):

        chance_crit, chance_hit, chance_graze = [ChanceCalculator.chance(c, precision, evasion) for c in initial_chances]
        return chance_crit, chance_hit, chance_graze
