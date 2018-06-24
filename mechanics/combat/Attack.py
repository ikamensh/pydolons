class Attack:
    @staticmethod
    def attack(source, target):
        damage = source.get_melee_damage()
        return target.recieve_damage(damage)

    @staticmethod
    def unarmed_attack(source, target):
        damage = source.get_unarmed_damage()
        return target.recieve_damage(damage)