class Unit:
    HP_PER_STR = 25
    MANA_PER_INT = 15
    UNARMED_DAMAGE_PER_STR = 5
    
    def __init__(self, baseType):
        self.str = baseType.str
        self.agi = baseType.agi
        self.int = baseType.int
        self.type_name = baseType.type_name
        self.reset()
        
    def reset(self):
        self.health = self.str * Unit.HP_PER_STR
        self.mana = self.int * Unit.MANA_PER_INT

    def get_unarmed_damage(self):
        return self.str * Unit.UNARMED_DAMAGE_PER_STR

    def recieve_damage(self, damage):
        """
        :param damage: amount of incoming damage
        :return: True if unit dies, False otherwise
        """
        self.health -= damage
        if self.health <= 0:
            return True
        else:
            return False

    def __repr__(self):
        return "{} with {} HP".format(self.type_name, self.health)