from mechanics.damage import Damage, DamageTypes, deal_damage

class FireDamagePerIntelligence:

    @staticmethod
    def apply(source, target):
        damage = Damage(source.int*5, DamageTypes.FIRE)
        deal_damage(damage, target, source=source)