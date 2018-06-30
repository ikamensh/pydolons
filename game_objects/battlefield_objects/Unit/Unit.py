from mechanics.damage import Damage
from mechanics.damage import Resistances, Armor
from game_objects.items import Inventory

class Unit:
    HP_PER_STR = 25
    STAMINA_PER_STR = 5
    MANA_PER_INT = 15
    UNARMED_DAMAGE_PER_STR = 5
    
    def __init__(self, baseType):
        self.str = baseType.str
        self.agi = baseType.agi
        self.int = baseType.int
        self.type_name = baseType.type_name
        self.actives = baseType.actives
        self.unarmed_damage_type = baseType.unarmed_damage_type
        self.resists = Resistances(baseType.resists)
        self.armor = Armor(baseType.armor_base, baseType.armor_dict)
        self.inventory = Inventory(baseType.inventory_capacity)
        self.equipment = baseType.equipment_cls()

        self.reset()


    def give_active(self, active):
        self.actives.add(active)
        active.assign_to_unit(self)

    #TODO create target method that prompts the game to get right kind of targeting from the user
    def activate(self, active, user_targeting):
        assert active in self.actives
        active.activate(user_targeting)

    def reset(self):
        self.health = self.str * Unit.HP_PER_STR
        self.mana = self.int * Unit.MANA_PER_INT
        self.stamina = self.str * Unit.STAMINA_PER_STR

    def get_unarmed_damage(self):
        return Damage(amount=self.str * Unit.UNARMED_DAMAGE_PER_STR, type=self.unarmed_damage_type)

    def get_melee_damage(self):
        return self.get_unarmed_damage()

    def can_pay(self, cost):
        result = True
        if cost.mana_cost > self.mana:
            result = False
        if cost.stamina_cost > self.stamina:
            result = False

        return result

    def pay(self, cost):
        self.mana -= cost.mana_cost
        self.stamina -= cost.stamina_cost

    def lose_health(self, dmg_amount):
        """
        :param dmg_amount: amount of incoming damage
        :return: True if unit dies, False otherwise
        """
        self.health -= dmg_amount
        if self.health <= 0:
            return True
        else:
            return False

    def __repr__(self):
        return "{} with {} HP".format(self.type_name, self.health)