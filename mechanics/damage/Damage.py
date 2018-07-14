from mechanics.chances.CritHitGrazeMiss import ImpactFactor


class Damage:
    protection_coef = {
        ImpactFactor.CRIT: 0.7,
        ImpactFactor.HIT: 1.0,
        ImpactFactor.GRAZE: 1.4
    }

    effect_coef = {
        ImpactFactor.CRIT: 2,
        ImpactFactor.HIT: 1,
        ImpactFactor.GRAZE: 0.5
    }

    def __init__(self, amount, type):
        self.amount = amount
        self.type = type

    @staticmethod
    def calculate_damage(damage, target, impact_factor=ImpactFactor.HIT):
        dmg_type = damage.type

        resist = target.resists[dmg_type]
        armor = target.armor[dmg_type] * \
                Damage.protection_coef[impact_factor]

        damage_final = int(max((damage.amount - armor) * (1 - resist), 0) *
                           Damage.effect_coef[impact_factor])

        return damage_final









