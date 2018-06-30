from mechanics.damage import deal_damage

class Attack:
    @staticmethod
    def attack(source, target):
        damage = source.get_melee_damage()
        return deal_damage(damage, target)

    @staticmethod
    def unarmed_attack(source, target):
        damage = source.get_unarmed_damage()
        return deal_damage(damage, target)