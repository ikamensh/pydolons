from mechanics.damage import DamageTypes
from character.masteries import MasteriesEnum

from mechanics.chances.CritHitGrazeMiss import ImpactChances

baseline_chances = ImpactChances(0.05, 0.35, 0.5)


def chances_price(chances: ImpactChances):

    crit_awesomeness = 0.2 + chances.crit / baseline_chances.crit
    hit_awesomeness = 0.2 + chances.hit / baseline_chances.hit
    graze_awesomeness = 0.2 + chances.crit / baseline_chances.graze

    return (crit_awesomeness * 2 + hit_awesomeness **
            5 + graze_awesomeness ** 5) / 5


class WeaponType:
    def __init__(
            self,
            damage_type,
            mastery,
            chances,
            damage_factor=1.,
            atb_factor=1.,
            cost_factor=1):
        self.damage_type = damage_type
        self.mastery = mastery
        self.chances = chances
        self.damage_factor = damage_factor
        self.atb_factor = atb_factor

        self.cost_factor = cost_factor * \
            chances_price(chances) * (1 + damage_factor ** 2 / (atb_factor ** (2 / 3))) / 2


d = DamageTypes
m = MasteriesEnum


class WeaponTypes:
    AXE = WeaponType(
        d.SLASH,
        m.AXE,
        ImpactChances(
            0.05,
            0.3,
            0.7),
        damage_factor=1.3,
        atb_factor=1.6)
    SWORD = WeaponType(d.SLASH, m.SWORD, ImpactChances(0.05, 0.4, 0.5))
    DAGGER = WeaponType(
        d.PIERCE,
        m.DAGGER,
        ImpactChances(
            0.10,
            0.3,
            0.2),
        damage_factor=0.7,
        atb_factor=0.45)
    SPEAR = WeaponType(d.PIERCE, m.SPEAR, ImpactChances(0.05, 0.4, 0.5))
    HAMMER = WeaponType(
        d.CRUSH,
        m.HAMMER,
        ImpactChances(
            0.1,
            0.35,
            0.25),
        damage_factor=1.5,
        atb_factor=2.1)
    CLUB = WeaponType(d.CRUSH, m.CLUB, ImpactChances(0.07, 0.37, 0.47))

    BOW = WeaponType(
        d.PIERCE,
        m.BOW,
        ImpactChances(
            0.02,
            0.25,
            0.25),
        cost_factor=3)
    CROSSBOW = WeaponType(
        d.PIERCE,
        m.SHOOT,
        ImpactChances(
            0.02,
            0.25,
            0.25),
        damage_factor=1.5,
        atb_factor=2.1,
        cost_factor=3)


if __name__ == "__main__":
    wts = WeaponTypes
    for wt in [
            wts.AXE,
            wts.SWORD,
            wts.DAGGER,
            wts.SPEAR,
            wts.HAMMER,
            wts.CLUB,
            wts.BOW,
            wts.CROSSBOW]:
        print(wt.cost_factor)
