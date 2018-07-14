from mechanics.damage import Damage, DamageTypes, DamageEvent

class FireDamage50:
    fixed_damage = Damage(50, DamageTypes.FIRE)

    @staticmethod
    def apply(source, target):
        DamageEvent(FireDamage50.fixed_damage, target, source=source)