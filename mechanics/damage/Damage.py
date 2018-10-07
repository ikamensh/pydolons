from mechanics.chances.CritHitGrazeMiss import ImpactFactor

class Damage:
    protection_coef = {
        ImpactFactor.CRIT: 0.7,
        ImpactFactor.HIT: 1.0,
        ImpactFactor.GRAZE: 1.4
    }

    effect_coef = {
        ImpactFactor.CRIT: 1.5,
        ImpactFactor.HIT: 1,
        ImpactFactor.GRAZE: 0.66
    }

    def __init__(self, amount, type):
        self.amount = amount
        self.type = type

    def __mul__(self, other):
        return Damage(self.amount*other, self.type)

    def __imul__(self, other):
        return Damage(self.amount * other, self.type)

    @staticmethod
    def calculate_damage(damage, target, impact_factor=ImpactFactor.HIT):
        dmg_type = damage.type

        resist = target.resists[dmg_type]
        armor = target.armor[dmg_type] * \
                Damage.protection_coef[impact_factor]

        damage_final = int(max((damage.amount - armor) * (1 - resist), 0) *
                           Damage.effect_coef[impact_factor])
        # print(damage_final)
        return damage_final, \
               Damage.calculate_armor_dur_damage(damage_final, armor, target.max_health), \
               Damage.calculate_weapon_dur_damage(damage.amount, damage_final, impact_factor)

    @staticmethod
    def calculate_expected_damage(chances, damage, target):

        result = 0
        chance_crit, chance_hit, chance_graze = chances
        running_chance = 1

        result += Damage.calculate_damage(damage, target, ImpactFactor.CRIT)[0] * chance_crit
        running_chance *= (1-chance_crit)
        result += Damage.calculate_damage(damage, target, ImpactFactor.HIT)[0] * chance_hit
        running_chance *= (1-chance_hit)
        result += Damage.calculate_damage(damage, target, ImpactFactor.GRAZE)[0] * chance_graze

        return result



    @staticmethod
    def calculate_armor_dur_damage(final_damage, armor_amount, target_hp):
        if final_damage == 0:
            return 0
        return int(5 * final_damage / (armor_amount + target_hp/final_damage))

    @staticmethod
    def calculate_weapon_dur_damage(damage_initial, damage_final, impact_factor):
        assert damage_initial > 0
        assert damage_final >= 0
        reduction = damage_initial * Damage.effect_coef[impact_factor] - damage_final
        reduction_over_threshold = reduction - 0.33 * damage_initial
        if reduction_over_threshold > 0:
            return int(5 * (reduction_over_threshold / damage_initial))
        else:
            return 0


    def __repr__(self):
        return f"{self.amount:.1f} of {self.type} damage"
