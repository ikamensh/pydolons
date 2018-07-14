from mechanics.damage import Damage, DamageTypes, DamageEvent

class FireDamagePerIntelligence:

    @staticmethod
    def apply(source, target):
        damage = Damage(source.int*5, DamageTypes.FIRE)
        DamageEvent(damage, target, source=source)