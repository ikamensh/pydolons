from mechanics.damage import deal_damage
from mechanics.events.Event import AttackStartedEvent
from mechanics.PrecisionEvasion.CritHitGrazeMiss import ImpactCalculator, ImpactFactor
from game_objects.battlefield_objects.Unit.Unit import Unit

class Attack:
    #Once weapons are implemented: get damage by weapon, pass weapon to attack event.

    @staticmethod
    def attack(source, target):
        damage = source.get_melee_damage()
        return Attack.__attack(source, target, damage)

    @staticmethod
    def unarmed_attack(source, target):
        damage = source.get_unarmed_damage()
        return Attack.__attack(source,target,damage)


    @staticmethod
    def __attack(source : Unit, target : Unit, damage):
        AttackStartedEvent(source, target)
        impact = ImpactCalculator.roll_impact(source.unarmed_chances, source.melee_precision, target.melee_evasion)
        if impact is not ImpactFactor.MISS:
            return deal_damage(damage, target, source=source, impact_factor = impact)
        else:
            print("MISS")

