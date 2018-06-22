from mechanics.battle.attack import Attack

class AttackEffect:
    @staticmethod
    def apply(source, target):
        Attack.attack(source, target)