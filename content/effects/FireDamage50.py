from mechanics.damage import Damage, DamageTypes, deal_damage

class FireDamage50:
    fixed_damage = Damage(50, DamageTypes.FIRE)

    @staticmethod
    def apply(source, target):
        deal_damage(FireDamage50.fixed_damage, target, source=source)