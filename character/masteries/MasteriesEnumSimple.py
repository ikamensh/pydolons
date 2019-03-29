from my_utils.named_enums import NameEnum, auto
from functools import lru_cache


class MasteriesEnum(NameEnum):
    AXE = auto()
    SWORD = auto()
    DAGGER = auto()

    SPEAR = auto()
    CLUB = auto()
    HAMMER = auto()

    UNARMED = auto()

    FIRE = auto()
    FROST = auto()
    LIGHTNING = auto()

    EARTH = auto()
    ACID = auto()
    AIR = auto()

    LIGHT = auto()
    ASTRAL = auto()
    NATURE = auto()

    MIND = auto()
    HOLY = auto()
    DARK = auto()

    SONIC = auto()
    BOW = auto()
    SHOOT = auto()


class MasteriesGroups:

    m = MasteriesEnum
    chop_chop_chop = [m.AXE, m.HAMMER, m.SWORD]
    stabby = [m.DAGGER, m.SPEAR]
    bashy = [m.CLUB, m.HAMMER, m.UNARMED]
    sniping = [m.BOW, m.SHOOT, m.LIGHT, m.SPEAR]
    spicky = [m.SPEAR, m.LIGHTNING, m.LIGHT]
    loud = [m.SONIC, m.HAMMER, m.EARTH, m.UNARMED]
    explosive = [m.FIRE, m.EARTH, m.SONIC, m.AXE, m.SHOOT]
    cold = [m.SWORD, m.DAGGER, m.FROST]
    arcane = [m.MIND, m.ASTRAL]
    chemical = [m.ACID, m.EARTH, m.SHOOT]
    all_battle = [m.CLUB, m.SWORD, m.AXE, m.DAGGER, m.SPEAR, m.UNARMED,
                  m.BOW, m.HAMMER, m.SHOOT]

    all_magic = [m.FROST, m.FIRE, m.LIGHT, m.LIGHTNING, m.EARTH,
                 m.ACID, m.SONIC, m.ASTRAL, m.MIND, m.HOLY, m.DARK, m.NATURE]

    all = [chop_chop_chop, stabby, bashy,
           sniping, spicky, loud, cold,
           arcane, chemical, explosive, all_battle, all_magic]

    coupling_coef = 0.5

    @classmethod
    @lru_cache()
    def occurances(cls, m):
        n = 0
        for lst in cls.all:
            for member in lst:
                if member is m:
                    n += 1

        return n

    @classmethod
    @lru_cache()
    def total_occurances(cls):
        result = 0
        for m in MasteriesEnum:
            result += cls.occurances(m)

        return result

    @classmethod
    @lru_cache(maxsize=2048)
    def coupling(cls, m1, m2):
        coupling = 0
        for group in cls.all:
            if m1 in group and m2 in group:
                coupling += 1

        return coupling * cls.coupling_coef / \
            (1 + cls.occurances(m1) + cls.occurances(m2))


if __name__ == "__main__":
    for m in MasteriesEnum:
        print(m, MasteriesGroups.occurances(m))
    print(MasteriesGroups.total_occurances())

    for m1 in MasteriesEnum:
        for m2 in MasteriesEnum:
            print(m1, m2, MasteriesGroups.coupling(m1, m2))
