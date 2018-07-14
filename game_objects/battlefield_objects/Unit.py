from game_objects.battlefield_objects.CharAttributes import CharAttributes


from game_objects.battlefield_objects.BaseType import BaseType
from game_objects.items import Inventory
from mechanics.attributes import Attribute, BonusAttributes
from mechanics.damage import Damage
from mechanics.damage import Resistances, Armor


class Unit:
    HP_PER_STR = 25
    STAMINA_PER_STR = 5
    MANA_PER_INT = 15
    UNARMED_DAMAGE_PER_STR = 5
    
    def __init__(self, base_type: BaseType):
        self.str_base = Attribute(base_type.attributes[CharAttributes.STREINGTH], 100, 0)
        self.end_base = Attribute(base_type.attributes[CharAttributes.ENDURANCE], 100, 0)
        self.prc_base = Attribute(base_type.attributes[CharAttributes.PERCEPTION], 100, 0)
        self.agi_base = Attribute(base_type.attributes[CharAttributes.AGILITY], 100, 0)
        self.int_base = Attribute(base_type.attributes[CharAttributes.INTELLIGENCE], 100, 0)
        self.cha_base = Attribute(base_type.attributes[CharAttributes.CHARISMA], 100, 0)


        self.type_name = base_type.type_name
        self.actives = base_type.actives
        self.unarmed_damage_type = base_type.unarmed_damage_type
        self.unarmed_chances = base_type.unarmed_chances
        self.resists = Resistances(base_type.resists)
        self.armor = Armor(base_type.armor_base, base_type.armor_dict)
        self.inventory = Inventory(base_type.inventory_capacity)
        self.equipment = base_type.equipment_cls()
        self.abilities = []
        self.alive = True

        self.icon = base_type.icon

        self.reset()



    def sum_with_abilities(self, base, attrib_enum):
        attr = base
        for ability in self.abilities:
            bonus = ability[attrib_enum]
            if bonus:
                attr += bonus
        return attr.value()

    @property
    def str(self):
        return self.sum_with_abilities(self.str_base, BonusAttributes.STR)

    @property
    def agi(self):
        return self.sum_with_abilities(self.agi_base, BonusAttributes.AGI)

    @property
    def int(self):
        return self.sum_with_abilities(self.int_base, BonusAttributes.INT)

    @property
    def end(self):
        return self.sum_with_abilities(self.int_base, BonusAttributes.END)

    @property
    def prc(self):
        return self.sum_with_abilities(self.int_base, BonusAttributes.PRC)

    @property
    def cha(self):
        return self.sum_with_abilities(self.int_base, BonusAttributes.CHA)

    @property
    def max_health(self):
        return self.sum_with_abilities(Attribute(self.str * Unit.HP_PER_STR, 100, 0), BonusAttributes.HEALTH)

    @property
    def max_mana(self):
        return self.sum_with_abilities(Attribute(self.int * Unit.MANA_PER_INT, 100, 0), BonusAttributes.MANA)

    @property
    def max_stamina(self):
        return self.sum_with_abilities(Attribute(self.str * Unit.STAMINA_PER_STR, 100, 0), BonusAttributes.STAMINA)

    @property
    def melee_precision(self):
        return self.str + self.agi

    @property
    def melee_evasion(self):
        return self.prc + self.agi

    def reset(self):
        self.health = self.max_health
        self.health_max_old = self.health

        self.mana = self.max_mana
        self.mana_max_old = self.mana

        self.stamina = self.max_stamina
        self.stamina_max_old = self.stamina

    def rescale(self):

        self.health = self.health * (self.max_health / self.health_max_old)
        self.health_max_old = self.max_health

        self.mana = self.mana * (self.max_mana / self.mana_max_old)
        self.mana_max_old = self.max_mana

        self.stamina = self.stamina * (self.max_stamina / self.stamina_max_old)
        self.stamina_max_old = self.max_stamina


    def give_active(self, active):
        self.actives.add(active)
        active.assign_to_unit(self)

    #TODO create target method that prompts the game to get right kind of targeting from the user
    def activate(self, active, user_targeting):
        assert active in self.actives
        active.activate(user_targeting)



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
        :return: True if unit lost all HP, False otherwise
        """
        assert dmg_amount >= 0
        self.health -= dmg_amount
        if self.health <= 0:
            return True
        else:
            return False


    def __repr__(self):
        return "{} with {} HP".format(self.type_name, self.health)